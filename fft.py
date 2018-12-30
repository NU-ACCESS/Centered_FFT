#centered fft and ifft returned as complex values. Uses Piotr Wendykier's Parallel FFTJ https://sites.google.com/site/piotrwendykier/software/parallelfftj
#for more on centering fft see https://dsp.stackexchange.com/questions/9039/centering-zero-frequency-for-discrete-fourier-transform		

def fft(imp,imp2,width,height):
	from edu.emory.mathcs.parallelfftj import DoubleTransformer
	from edu.emory.mathcs.parallelfftj import SpectrumType
	from ij import IJ, ImagePlus, ImageStack
	from ij.process import ImageProcessor, FloatProcessor
	import cmath, math
	#convert inputs into a complex field
	b = [complex(x , y) for x , y in zip([val for val in imp.getProcessor().getPixels()],[val for val in imp2.getProcessor().getPixels()])]
	#f1 = []
	#for x in range(N):
	#	for y in range(N):
	#		f = cmath.exp(-1j*math.pi*(x + y))
	#		f1.append(f)
	#old for loop above. More efficient list comprhension below. 	
	f1 = [cmath.exp(-1j*math.pi*(x + y)) for x in range(width) for y in range(height)]
	
	imp_r = ImagePlus("real", FloatProcessor(width,height,[(x * y).real for x , y in zip(f1, b)]))
	imp_i = ImagePlus("IMAGINARY", FloatProcessor(width,height,[(x * y).imag for x , y in zip(f1, b)]))

	FFT1 = DoubleTransformer(imp_r.getStack(), imp_i.getStack())
	FFT1.fft()
	r = FFT1.toImagePlus(SpectrumType.REAL_PART)
	i = FFT1.toImagePlus(SpectrumType.IMAG_PART)
	a = [complex(x , y) for x , y in zip([val for val in r.getProcessor().getPixels()],[val for val in i.getProcessor().getPixels()])]
	c = [(x * y) for x , y in zip(f1, a)]
	return(c)

def ifft(imp,imp2,width,height):	
	from edu.emory.mathcs.parallelfftj import DoubleTransformer
	from edu.emory.mathcs.parallelfftj import SpectrumType
	from ij import IJ, ImagePlus, ImageStack
	from ij.process import ImageProcessor, FloatProcessor
	import cmath, math	
	b = [complex(x , y) for x , y in zip([val for val in imp.getProcessor().getPixels()],[val for val in imp2.getProcessor().getPixels()])]
	
	f1 = [cmath.exp(-1j*math.pi*(x + y)) for x in range(width) for y in range(height)] #See forward fft for old centering loop. 

	imp_r = ImagePlus("real", FloatProcessor(width,height,[(x * y).real for x , y in zip(f1, b)]))
	imp_i = ImagePlus("IMAGINARY", FloatProcessor(width,height,[(x * y).imag for x , y in zip(f1, b)]))

	FFT1 = DoubleTransformer(imp_r.getStack(), imp_i.getStack())
	FFT1.ifft(1)#returns either unweighted or weighted
	r = FFT1.toImagePlus(SpectrumType.REAL_PART)
	i = FFT1.toImagePlus(SpectrumType.IMAG_PART)
	a = [complex(x , y) for x , y in zip([val for val in r.getProcessor().getPixels()],[val for val in i.getProcessor().getPixels()])]
	c = [(x * y) for x , y in zip(f1, a)]
	return(c)