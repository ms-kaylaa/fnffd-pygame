#version 330 core
uniform sampler2D image;

out vec4 color;
in vec2 fragmentTexCoord;

uniform vec4 colorreplace;
uniform vec3 ignoreRGB;

void main() {
    vec4 pixelcheck = texture(image, fragmentTexCoord);

    if(abs(pixelcheck.a) > 0.0 && pixelcheck.rgb != ignoreRGB) {
        pixelcheck = vec4((colorreplace.a * colorreplace.rgb + (1 - colorreplace.a) * pixelcheck.rgb), pixelcheck.a);
    }

    color = pixelcheck;
}
