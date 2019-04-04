#This function will return the points of a hilbert curve

"""
Credit goes to Dylan Grafmyre for his code for the three js library found here:
    https://threejs.org/examples/webgl_lines_colors.html

Also, credit to Thomas Diedwald, whose work was the basis for Dylan
Link: http://www.openprocessing.org/visuals/?visualID=15599
"""

def Hilbert3D(center = (0,0,0), size = 10, iterations = 1,
              v0=0,v1=1,v2=2,v3=3,v4=4,v5=5,v6=6,v7=7):
    #base model will only work with 1 iterations
    #size = 10
    half = size / 2
    #iterations = 1
    #v0 = 0
    #v1 = 1
    #v2 = 2
    #v3 = 3
    #v4 = 4
    #v5 = 5
    #v6 = 6
    #v7 = 7

    vec_s = [
        (center[0] - half, center[1] + half, center[2] - half),
        (center[0] - half, center[1] + half, center[2] + half),
        (center[0] - half, center[1] - half, center[2] + half),
        (center[0] - half, center[1] - half, center[2] - half),
        (center[0] + half, center[1] - half, center[2] - half),
        (center[0] + half, center[1] - half, center[2] + half),
        (center[0] + half, center[1] + half, center[2] + half),
        (center[0] + half, center[1] + half, center[2] - half)
        ]

    vec = [
        vec_s[v0],
        vec_s[v1],
        vec_s[v2],
        vec_s[v3],
        vec_s[v4],
        vec_s[v5],
        vec_s[v6],
        vec_s[v7]
        ]

    #if iterations != 1, then recurse to find the points
    iterations -=1
    if((iterations) >= 0):
        tmp = []
        tmp += Hilbert3D(vec[0],half,iterations,v0, v3, v4, v7, v6, v5, v2, v1)
        tmp += Hilbert3D(vec[1],half,iterations,v0, v7, v6, v1, v2, v5, v4, v3 )
        tmp += Hilbert3D(vec[2],half,iterations,v0, v7, v6, v1, v2, v5, v4, v3 )
        tmp += Hilbert3D(vec[3],half,iterations,v2, v3, v0, v1, v6, v7, v4, v5 )
        tmp += Hilbert3D(vec[4],half,iterations,v2, v3, v0, v1, v6, v7, v4, v5)
        tmp += Hilbert3D(vec[5],half,iterations,v4, v3, v2, v5, v6, v1, v0, v7 )
        tmp += Hilbert3D(vec[6],half,iterations,v4, v3, v2, v5, v6, v1, v0, v7 )
        tmp += Hilbert3D(vec[7],half,iterations,v6, v5, v2, v1, v0, v3, v4, v7 )

        return tmp
    return vec
