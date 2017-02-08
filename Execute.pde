
// All these functions take the string "path" as an argument. This should be set to the path of the folder "vybe_interface" in your system."

void sendStop(String path) {
    exec("cd ", path);
    exec("cd", "vybe_demo");
    exec("python", "vybe_demo.py", "0","a");
}

void sendPoint(String path, int mode, float x, float y, float z) {
    exec("cd ", path);
    exec("cd", "vybe_demo");
    exec("python", "vybe_demo.py", str(mode),"a", str(x), str(y), str(z));
}

void sendMovement(String path, int mode, String axis) {
    exec("cd ", path);
    exec("cd", "vybe_demo");
    exec("python", "vybe_demo.py", str(mode), axis);
}