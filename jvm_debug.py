import jpype
import os
import sys

def start_jvm():
    jar_path = "py-tetrad/pytetrad/resources/tetrad-current.jar"
    
    # Check if JVM is already running
    if jpype.isJVMStarted():
        print("JVM already running")
        return True
    
    # Check if JAR exists
    if not os.path.exists(jar_path):
        print(f"JAR file not found at: {os.path.abspath(jar_path)}")
        return False
    
    try:
        print(f"Starting JVM with JAR: {jar_path}")
        jpype.startJVM(
            jpype.getDefaultJVMPath(),
            f'-Djava.class.path={jar_path}',
            '--enable-native-access=ALL-UNNAMED',
        )
        print("✓ JVM started successfully with native access enabled")
        return True
        
    except Exception as e:
        print(f"✗ JVM startup failed: {e}")
        return False

start_jvm()