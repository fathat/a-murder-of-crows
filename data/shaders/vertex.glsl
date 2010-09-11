varying vec4 location;
uniform mat3 transform;

void main()
{
    vec3 science = gl_Vertex.xyz;
    location = vec4(science.x, science.y, science.z, 1);
    gl_Position = ftransform();
}