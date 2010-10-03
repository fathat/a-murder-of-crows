varying vec4 worldCoords;
varying vec4 localCoords;
uniform mat3 transform;

void main()
{
	worldCoords = gl_ModelViewMatrix * gl_Vertex; 
    localCoords = gl_Vertex;
    gl_Position = ftransform();
}