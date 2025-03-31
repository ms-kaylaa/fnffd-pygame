#version 330 core
uniform sampler2D image;

out vec4 color;
in vec2 fragmentTexCoord;

uniform vec4 colorreplace;

void main() {
    vec4 pixelcheck = texture(image, fragmentTexCoord);

    if(abs(pixelcheck.a) > 0.0) {
        pixelcheck.rgb = colorreplace.rgb; //replace color
    }

    color = pixelcheck;
}
