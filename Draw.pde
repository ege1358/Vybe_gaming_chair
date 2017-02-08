void setScreen() {
  float cameraY = height/2.0;
  float cameraZ = cameraY / tan(fov / 2.0);
  float aspect = float(width)/float(height);
  perspective(fov, aspect, cameraZ/10.0, cameraZ*10.0);
  
  if(mousePressed){
      if(first) {
        mouse_ix = mouseX;
        mouse_iy = mouseY;
        first = false;
      }
    mouse_y = mouseY;
    mouse_x = mouseX;
  }
  else {
    first = true;
    mouse_ly = mouse_ly+(mouse_y-mouse_iy);
    mouse_y = 0;
    mouse_iy = 0;
    mouse_lx = mouse_lx+(mouse_x-mouse_ix);
    mouse_x = 0;
    mouse_ix = 0;
  }  
  translate(360,300,0);
  rotateX(PI/3 + (mouse_ly+(mouse_y-mouse_iy))/float(height) * PI);
  rotateY(PI/3 + (mouse_lx+(mouse_x-mouse_ix))/float(width) * 2 * PI);
  stroke(0,0,255);
  line(0,720,0,0,-720,0);
  
  stroke(255,0,0);
  line(-720,0,0,720,0,0);
  
  stroke(0,255,0);
  line(0,0,720,0,0,-720);
  
  stroke(255);
  rect(-40,-100,80,100);
  
  pushMatrix();
    rotateX(PI/2);
    rotateZ(PI/2); 
    rect(0,-40,60,80);
  popMatrix();
  
  for(int i = -720; i <= 720; i+= 20) {
    if(i != 0) {
      stroke(0,0,255);
      line(-10,i,0,10,i,0);
      stroke(255,0,0);
      line(i,0,-10,i,0,10);
      stroke(0,255,0);
      line(-10,0,i,10,0,i);
    }
  }
}

void mouseWheel(MouseEvent event) {
  float e = event.getCount();
  fov += e/1000 * PI/2;
  if (fov > 2.0) {
    fov = 2.0; 
  }
  else if (fov < 0.3) {
    fov = 0.3; 
  }
}

void addPoint(float x, float y, float z, String text) {
  pushMatrix();
  translate(x*20,y*20,z*20); 
  stroke(255);
  sphere(10);
  fill(255);
  /*translate(0,0,30);
  rotateX(-PI/3 - (mouse_ly+(mouse_y-mouse_iy))/float(height) * PI);
  rotateY(-PI/3 - (mouse_lx+(mouse_x-mouse_ix))/float(width) * 2 * PI);
  text(text,0,0);
  fill(255,69,0);
  stroke(0);
  */
  popMatrix();
}

void addArrow(float x1, float y1, float z1, float x2, float y2, float z2) {
  pushMatrix();
  translate(x1*20,y1*20,z1*20);
  rotateX(atan((y2-y1)/(x2-x1)));
  rotateZ(atan((z2-z1)/sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))));
  float distance = 20*sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1)+(z2-z1)*(z2-z1));
  
  beginShape(TRIANGLE_FAN);
  for(int i = 0; i < 36; i++) {
    vertex(10*cos(radians(i*10)),10*sin(radians(i*10)),0); 
  }
  endShape();
  
  beginShape(QUAD_STRIP);
  for(int i = 0; i < 36; i++) {
    vertex(10*cos(radians(i*10)),10*sin(radians(i*10)),0); 
    vertex(10*cos(radians(i*10)),10*sin(radians(i*10)),distance-10); 
  }
  endShape();
  
  beginShape(TRIANGLE_FAN);
  for(int i = 0; i < 36; i++) {
    vertex(10*cos(radians(i*10)),10*sin(radians(i*10)),distance-10); 
  }
  endShape();
  
  beginShape(QUAD_STRIP);
  for(int i = 0; i < 36; i++) {
    vertex(15*cos(radians(i*10)),15*sin(radians(i*10)),distance-10); 
    vertex(0,0,distance+10); 
  }
  endShape();
  
  stroke(255);
  popMatrix();
}