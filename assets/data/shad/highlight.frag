#version 330 core
uniform sampler2D image;

out vec4 color;
in vec2 fragmentTexCoord;

uniform vec3 toHighlight;
uniform vec3 highlightWith;

void main() {
    vec4 defColor = texture(image, fragmentTexCoord);
    if((defColor.rgb == toHighlight)) {
        color = vec4(highlightWith, defColor.a);
    } else {
        color = defColor;
    }
}