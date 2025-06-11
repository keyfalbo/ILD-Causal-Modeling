import numpy as np
import pandas as pd

from numpy.linalg import svd, inv, cholesky

from jpype import JImplements, JOverride

import java.util as util
import edu.cmu.tetrad.data as td
from edu.cmu.tetrad.search.score import Score


@JImplements(Score)
class DG:

    def __init__(self, df, discount=1.0):
        self.n, self.p = df.shape
        self.cols = list(df.columns)
        self.discount = discount
        self.col_map = {}
        self.nodes = util.ArrayList()
        self.node_map = {}

        discrete = []
        for col in self.cols:
            if np.issubdtype(df[col].dtype, np.inexact): continue
            discrete.append(col)

        cat_map = {}
        for col in discrete:
            cats = [x for x in df[col].unique() if not np.isnan(x)]
            cat_map[col] = {cat: i for i, cat in enumerate(cats)}

        df = df.replace(cat_map)

        idx = 0
        for col in self.cols:
            if col in discrete:
                cats = util.ArrayList()
                for cat in cat_map[col]: cats.add(str(cat))
                card = len(cat_map[col]) - 1
                if not card: continue
                self.col_map[col] = [idx + i for i in range(card)]
                idx += card
                node = td.DiscreteVariable(str(col), cats)
                self.nodes.add(node)
                self.node_map[col] = node
            else:
                self.col_map[col] = [idx]
                idx += 1
                node = td.ContinuousVariable(str(col))
                self.nodes.add(node)
                self.node_map[col] = node

        self.df = pd.DataFrame(np.zeros([self.n, idx]))

        idx = 0
        for col in self.cols:
            card = len(self.col_map[col])
            if card == 1:
                self.df[idx] = df[col]
            else:
                for i in self.col_map[col]:
                    data = [np.nan if np.isnan(x) 
                            else float(x == cat_map[col][i - idx]) 
                            for x in df[col]]
                    self.df[i] = data
            idx += card

        self.cov = self.df.cov().values

    def setPenaltyDiscount(self, discount):
        self.discount = discount

    @JOverride
    def localScore(self, *args):
        ch = self.col_map[self.cols[args[0]]]
        pa = []

        if len(args) == 1:
            pass
        elif isinstance(args[1], int):
            pa = self.col_map[self.cols[args[1]]]
        else:
            for i in args[1]: pa += self.col_map[self.cols[i]]

        # Testwise deletion
        # df = self.df[pa + ch].dropna()
        # n, p = df.shape
        # S = df.cov().values
        # k = len(pa)

        # Alternative
        idx = np.ix_(pa + ch, pa + ch)
        S = self.cov[idx]
        n = self.n
        p = len(pa + ch)
        k = len(pa)


        # N.J. Higham, "Computing a nearest symmetric positive definite
        # matrix" (1988): https://doi.org/10.1016/0024-3795(88)90223-6
        # https://www.mathworks.com/matlabcentral/fileexchange/42885-nearestspd
        # A = (S + S.T) / 2
        # _, s, VT = svd(A)
        # H = VT.T @ np.diag(s) @ VT
        # A = (A + H) / 2
        # Shat = (A + A.T) / 2

        # Alternative projection: fix the smallest singular values
        U, s, VT = svd(S)
        s = np.clip(s, a_min=1e-3, a_max=None)
        Shat = U @ np.diag(s) @ VT

        lik = -len(ch) * np.log(2 * np.pi) / 2

        L = cholesky(Shat)
        D = np.diag(L)
        lik -= np.sum(np.log(D[k:]))

        Li = inv(L)
        lik -= np.trace(Li.T @ S @ Li) / (n * 2)

        if len(pa):
            idx = np.ix_(range(k), range(k))
            Li = inv(L[idx])
            lik += np.trace(Li.T @ S[idx] @ Li) / (n * 2)

        dof = p * (p - 1) / 2
        dof -= k * (k - 1) / 2
        penalty = self.discount * (dof / 2) * (np.log(n) / n)
        score = lik - penalty

        return score
    
    def setPenaltyDiscount(self, penalty_discount):
        self.l = penalty_discount 


    @JOverride
    def localScoreDiff(self, *args):
        ch = args[0]
        pa = []

        if len(args) > 2:
            for i in args[2]: pa.append(i)

        diff = -self.localScore(ch, pa)
        pa.append(args[1])
        diff += self.localScore(ch, pa)

        return diff

    @JOverride
    def getVariables(self):
        return self.nodes

    @JOverride
    def getSampleSize(self):
        return self.n

    @JOverride
    def toString(self):
        return "Degenerate Gaussian"

    @JOverride
    def getVariable(self, targetName):
        if targetName in self.node_map:
            return self.node_map[targetName]
        return None

    @JOverride
    def isEffectEdge(self, bump):
        return False

    @JOverride
    def getMaxDegree(self):
        return 1000

    @JOverride
    def defaultScore(self):
        return self
