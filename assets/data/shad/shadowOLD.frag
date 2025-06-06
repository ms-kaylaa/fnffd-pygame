#version 330 core
uniform sampler2D image;

out vec4 color;
in vec2 fragmentTexCoord;

uniform vec2 shadowOffset;
uniform vec4 shadowColor;

uniform vec3 ignoreRGB;

void main() {
    vec4 defColor = texture(image, fragmentTexCoord);
    if((defColor.rgb == ignoreRGB)) {
        if(defColor.rgb == ignoreRGB) {
            color = vec4(1, 1, 1, 1);
        } else color = defColor;
        return;
    }
    vec4 offsetColor = texture(image, fragmentTexCoord + shadowOffset);

    float offsetX = fragmentTexCoord.x + shadowOffset.x;
    float offsetY = fragmentTexCoord.y + shadowOffset.y;

    bool inBounds = (offsetX >= 0 && offsetY >= 0) && (offsetX <= 1 && offsetY <= 1);

    if (inBounds && offsetColor.a > 0) {
        color = vec4((shadowColor.a * shadowColor.rgb + (1 - shadowColor.a) * defColor.rgb), defColor.a);
    } else {
        color = defColor;
    }
}
