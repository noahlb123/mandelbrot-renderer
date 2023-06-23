import numpy as np
import multiprocessing
from PIL import Image
from matplotlib import cm

#all complex numbers are implemented using their vector definition
#a+bi = [[a,b],[-b,a]]
def makeComplex(a, b):
    return np.array([[a, b], [-b, a]])

#|a+bi|^2 = a^2+b^2
def complexMagnitude(c):
    return c[0][0]**2 + c[0][1]**2

#takes a complex vector c and gives number of iterations to escape bounds
#f(z) = z^2 + c
def mandle(c):
    iterations = 0
    z = np.array([[0, 0], [0, 0]])
    while iterations < maxIterations:
        if complexMagnitude(z) > 4:
            return iterations
        zsq = np.matmul(z, z)
        z = np.add(zsq, c)
        iterations += 1
    return 0

#wrapper for render calculations to simplify code
def wrapper(i, r, realMin, step, imMin):
    return mandle(makeComplex(realMin + step * r, imMin + step * i))

#renders mandlebrot given dimensions and saves image
def render(realMin, realMax, imMin, imMax, resolution):
    pool = multiprocessing.Pool()
    step = (realMax - realMin) / resolution
    imRes = int((imMax - imMin) / step)
    print("calculating...")
    result_async = [[pool.apply_async(wrapper, args = (i, r, realMin, step, imMin)) for r in range(resolution)] for i in range(imRes)]
    data = [[element.get() for element in array] for array in result_async]
    data = np.array(data).astype(np.int8)
    #data = np.uint8(cm.hsv(data)*255) <- to convert to color
    img = Image.fromarray(data)
    img = img.convert('L')
    img.save('output/Mandlebrot.png')

if __name__ == "__main__":
    realMin = input("enter minimum real coordinate: ")
    if realMin == "":
        maxIterations = 10000
        render(0.294687, 0.294776, 0.018231105, 0.018286730, 2560)
    else:
        realMin = float(realMin)
        realMax = float(input("enter maximum real coordinate: "))
        imMin = float(input("enter minimum imaginary coordinate: "))
        imMax = float(input("enter maximum imaginary coordinate: "))
        resolution = int(input("enter resolution (pixles): "))
        maxIterations = int(input("enter maximum iterations: "))
        render(realMin, realMax, imMin, imMax, resolution)
    print("done.")