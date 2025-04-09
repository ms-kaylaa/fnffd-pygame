#version 330 core
uniform sampler2D image;

out vec4 color;
in vec2 fragmentTexCoord;

uniform vec2 shadowOffset;
uniform vec4 shadowColor;
uniform vec2 shadowScale;

uniform vec3 ignoreRGB;

bool dropshadow = false; // mimic the 2-draw-call effect from free download... looks kinda bad cause frame widths get in the way but its an option regardless

void main() {
    vec4 defColor = texture(image, fragmentTexCoord);
    if((defColor.rgb == ignoreRGB) && (defColor.a > 0.0)) {
        color = defColor;
        return;
    }

    vec2 shadowScaleMod = vec2(shadowScale.x, shadowScale.y);

    // in case i was too LAZY to set the uniform!
    if(shadowScaleMod.x == 0.0) {
        shadowScaleMod.x = 1.0;
    }
    if(shadowScaleMod.y == 0.0) {
        shadowScaleMod.y = 1.0;
    }

    vec2 center = vec2(0.5, 0.5);
    vec2 scaledCoord = center + (fragmentTexCoord - center) * vec2(1.0/shadowScaleMod.x, 1.0/shadowScaleMod.y);
    vec2 offsetCoord = scaledCoord + shadowOffset;

    float offsetX = offsetCoord.x;
    float offsetY = offsetCoord.y;
    bool inBounds = (offsetX >= 0 && offsetY >= 0) && (offsetX <= 1 && offsetY <= 1);

    vec4 offsetColor = texture(image, offsetCoord);

    if (inBounds && (offsetColor.a > 0)) {
        float shadowadd = 0.0;
        if(dropshadow) shadowadd = shadowColor.a;
        color = vec4((shadowColor.a * shadowColor.rgb + (1 - shadowColor.a) * defColor.rgb), defColor.a+shadowadd);
    } else {
        color = defColor;
    }
}