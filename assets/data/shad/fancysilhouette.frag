#version 330 core
uniform sampler2D image;

out vec4 color;
in vec2 fragmentTexCoord;

uniform vec2 shadowOffset;
uniform vec4 shadowColor;

void main() {
    vec4 defColor = texture(image, fragmentTexCoord);
    vec4 offsetColor = texture(image, fragmentTexCoord + shadowOffset);

    if (offsetColor.a > 0 && defColor.a == 0) {
        color = shadowColor;
    } else {
        color = defColor;
    }
}
