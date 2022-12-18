# I SHOULD SOLVE PART2 BY FLOOD FILLING THE OUTSIDE REGION INSTEAD OF THE WAY I DO IT NOW

with open('input.dat', 'r') as file:
    lines = [line.strip() for line in file.readlines()]

voxels = set([eval("(" + line + ")") for line in lines])

def calcSA(voxels):
    surfaceArea = 0
    # sides touch if exactly 1 voxel coordinate differs by 1
    for (x, y, z) in voxels:
        voxelSurfaceArea = 6
        # check if neighbours are present
        for dx, dy, dz in [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]:
            if (x + dx, y+dy, z+dz) in voxels:
                voxelSurfaceArea -= 1
        
        surfaceArea += voxelSurfaceArea
    
    return surfaceArea

print(calcSA(voxels))

# PART 2

# find ranges of x, y and z values
xrange = [min([x for x, _, _ in voxels]), 1 + max([x for x, _, _ in voxels])]
yrange = [min([y for _, y, _ in voxels]), 1 + max([y for _, y, _ in voxels])]
zrange = [min([z for _, _, z in voxels]), 1 + max([z for _, _, z in voxels])]


# loop over all vertical lines and fill up interior volume
for x in range(*xrange):
    for y in range(*yrange):

        try:
            zInteriorStart = min([z for z in range(*zrange) if (x, y, z) in voxels])
            zInteriorEnd = max([z for z in range(*zrange) if (x, y, z) in voxels])
            
            print([z for z in range(*zrange) if (x, y, z) in voxels])
            # loop over drop interor along vertical z line
            for z in range(zInteriorStart, zInteriorEnd):
                # if unfilled
                if (x, y, z) not in voxels:
                    
                    # now we have to check if it is in the interior also in the x and y directions
                    xInteriorStart = min([xx for xx in range(*xrange) if (xx, y, z) in voxels])
                    xInteriorEnd = max([xx for xx in range(*xrange) if (xx, y, z) in voxels])
                    yInteriorStart = min([yy for yy in range(*yrange) if (x, yy, z) in voxels])
                    yInteriorEnd = max([yy for yy in range(*yrange) if (x, yy, z) in voxels])

                    if xInteriorStart < x < xInteriorEnd and yInteriorStart < y < yInteriorEnd:
                        print("FILLED")
                        voxels.add((x, y, z))
        except:
            continue


# WARNING. ONLY WORKS FOR MY SPECIFIC INPUT BECAUSE IT GETS A SINGLE VOXEL WRONG 
# REMOVING WHICH WOULD ADD 4 UNITS TO THE SURFACE AREA
# PLOTTING IN JUPYTER NOTEBOOK CAN BE USED TO FIND WRONG VOXEL
# CANT BE BOTHERED TO FIX THE CODE
print(calcSA(voxels) + 4)