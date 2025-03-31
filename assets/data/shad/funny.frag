#version 330 core
uniform sampler2D image;

out vec4 color;
in vec2 fragmentTexCoord;

void main() {
    vec4 funnyColor = texture(image, fragmentTexCoord);
    
    color = vec4(1.0*funnyColor.r, 0, 0, 1.0*funnyColor.a);
}