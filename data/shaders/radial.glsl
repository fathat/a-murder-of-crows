
uniform vec2 center;
uniform float radius;

uniform vec4 stops;

uniform vec4 stop0;
uniform vec4 stop1;
uniform vec4 stop2;
uniform vec4 stop3;
uniform vec4 stop4;

uniform mat3 worldTransform;
uniform mat3 gradientTransform;
uniform mat3 invGradientTransform;

varying vec4 worldCoords;
varying vec4 localCoords; 

void main()
{
    vec4 result;
    
    vec3 transformed = invGradientTransform*vec3(localCoords.x, localCoords.y, 1);
    
    //what is this actually doing?
    vec3 realcenter = vec3(center.x, center.y, 1);

    //calculate the intensity
    float intensity = clamp(distance(transformed.xy, realcenter.xy) / radius, 0.0, 1.0 );
    if(intensity <= stops.x)
    {
        result.rgba = mix(stop0, stop1, (intensity / stops.x));
    }
    else if(intensity <= stops.y)
    {
        result.rgba = mix(stop1, stop2, (intensity-stops.x) / (stops.y-stops.x));
    }
    else if(intensity <= stops.z)
    {
        result.rgba = mix(stop2, stop3, (intensity-stops.y) / (stops.z-stops.y));
    }
    else if(intensity <= stops.w)
    {
        result.rgba = mix(stop3, stop4, (intensity-stops.z) / (stops.w-stops.z));
    }
    
    gl_FragColor = result;
}