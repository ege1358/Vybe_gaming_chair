import at.mukprojects.console.*;
Console console;
boolean showConsole;

float mouse_ix = 0, mouse_iy = 0, mouse_lx = 0, mouse_ly = 0, mouse_x = 0, mouse_y = 0;
boolean first;
float fov = PI/2;

void setup() {
  size(720, 720, P3D);
  sendStop("/Users/Student/Desktop/vybe_interface");
}

int elapsed = millis();

void draw() {
  lights();
  background(100);
  setScreen();
  addPoint(10,10,10,"hi");
 
}