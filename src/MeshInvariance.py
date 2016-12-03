import numpy as np 
import trimesh

"""
Adapted from https://github.com/mikedh/trimesh
Mostly because we had problems compiling the rest of Trimesh
"""

_MIN_BIN_COUNT = 20
_TOL_FREQ = 1e-3

def zero_pad(data, count, right=True):
    """
    Params:
    	data: (n) length 1D array
    	count: int
    Returns:
    	padded: (count) length 1D array if (n < count), otherwise length (n)
    """
    if len(data) == 0:
        return np.zeros(count)
    elif len(data) < count:
        padded = np.zeros(count)
        if right:
            padded[-len(data):] = data
        else:
            padded[:len(data)] = data
        return padded
    else:
        return np.asanyarray(data)


def rotationally_invariant_identifier(mesh, length=6):
    """
    Given an input mesh, return a vector or string that has the following properties:
    * invariant to rotation of the mesh
    * robust to different tesselation of the surfaces
    * meshes that are similar but not identical return values that are close in euclidean distance
    Does this by computing the area- weighted distribution of the radius (from the center of mass).
    
    Params:
    	mesh:    Trimesh
    	length:  number of terms to compute of the identifier
    Returns:
    	identifer: (length) float array of unique identifier
    """

    frequency_count = int(length - 2)

    # calculate the mass properties of the mesh, which is doing a surface integral to
    # find the center of volume of the mesh
    mass_properties = mesh.mass_properties(skip_inertia=True)
    vertex_radii = np.sum((mesh.vertices.view(np.ndarray) - mesh.center_mass)**2,
                          axis=1) ** .5

    # since we will be computing the shape distribution of the radii, we need to make sure there
    # are enough values to populate more than one sample per bin.
    bin_count = int(np.min([256,
                            mesh.vertices.shape[0] * 0.2,
                            mesh.faces.shape[0] * 0.2]))

    # if any of the frequency checks fail, we will use this zero length vector as the
    # formatted information for the identifier
    freq_formatted = np.zeros(frequency_count)

    if bin_count > _MIN_BIN_COUNT:
        face_area = mesh.area_faces
        face_radii = vertex_radii[mesh.faces].reshape(-1)
        area_weight = np.tile(
                             (face_area.reshape((-1, 1)) * (1.0 / 3.0)), (1, 3)).reshape(-1)

        if face_radii.std() > 1e-3:
            freq_formatted = fft_freq_histogram(face_radii,
                                                bin_count=bin_count,
                                                frequency_count=frequency_count,
                                                weight=area_weight)

    # using the volume (from surface integral), surface area, and top
    # frequencies
    identifier = np.hstack((mass_properties['volume'],
                            mass_properties['surface_area'],
                            freq_formatted))
    return identifier



def fft_freq_histogram(data, bin_count, frequency_count=4, weight=None):
	"""
	Helper method for Rotational Invariance, performs FFT.
	"""
    data = np.reshape(data, -1)
    if weight is None:
        weight = np.ones(len(data))

    hist, bin_edges = np.histogram(data,
                                   weights=weight,
                                   bins=bin_count)
    # we calculate the fft of the radius distribution
    fft = np.abs(np.fft.fft(hist))
    # the magnitude is dependant on our weighting being good
    # frequency should be more solid in more cases
    freq = np.fft.fftfreq(data.size, d=(
        bin_edges[1] - bin_edges[0])) + bin_edges[0]

    # now we must select the top FREQ_COUNT frequencies
    # if there are a bunch of frequencies whose components are very close in magnitude,
    # just picking the top FREQ_COUNT of them is non-deterministic
    # thus we take the top frequencies which have a magnitude that is distingushable
    # and we zero pad if this means fewer values available
    fft_top = fft.argsort()[-(frequency_count + 1):]
    fft_ok = np.diff(fft[fft_top]) > _TOL_FREQ
    if fft_ok.any():
        fft_start = np.nonzero(fft_ok)[0][0] + 1
        fft_top = fft_top[fft_start:]
        freq_final = np.sort(freq[fft_top])
    else:
        freq_final = []

    freq_formatted = zero_pad(freq_final, frequency_count)
    return freq_formatted



def load(filename):
	return trimesh.load_mesh(filename)

