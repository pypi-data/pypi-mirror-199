"""


Library of functions for determining microscope properties.

"""
def get_psf(image_path):
    """
    Calculate the psf from z-stack images of fluorescent beads.
    
    Parameters
    ----------
    image_path : str
        Path to the tif file with a metadata header.

    Returns
    -------
    None.

    """
    import numpy as np
    from skimage.io import imread
    from pyclesperanto_prototype import imshow
    import pyclesperanto_prototype as cle
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    # Add way to specify the path
    
    if image_path in locals():
        image_path = image_path
    else:
        image_path = '/data/'
    bead_image = imread(image_path)
    
    # Channel 2 has the correct stack (green), channel 1 is not used
    green = 1
    red = 0
    
    # if bead_image has extra channel
    if len(bead_image > 3):
        bead_image_green = bead_image[green,:,:,:]
        bead_image_red = bead_image[red,:,:,:]
    else:
        bead_image_green = bead_image
        
    
    # Show the x,y,z projections
    #fig, axs = plt.subplot_mosaic(mosaic, fig_kw)
    imshow(cle.maximum_x_projection(bead_image_green), colorbar=True)
    imshow(cle.maximum_y_projection(bead_image_green), colorbar=True)
    imshow(cle.maximum_z_projection(bead_image_green), colorbar=True)
    
    # Segment objects
    label_image = cle.voronoi_otsu_labeling(bead_image_green)
    imshow(label_image, labels=True)
    
    # determine center of mass for each object
    stats = cle.statistics_of_labelled_pixels(bead_image_green, label_image)
    
    df = pd.DataFrame(stats)
    df[["mass_center_x", "mass_center_y", "mass_center_z"]]
    
    # configure size of future PSF image
    psf_radius = 20
    size = psf_radius * 2 + 1
    
    # initialize PSF
    single_psf_image = cle.create([size, size, size])
    avg_psf_image = cle.create([size, size, size])
    
    num_psfs = len(df)
    for index, row in df.iterrows():
        x = row["mass_center_x"]
        y = row["mass_center_y"]
        z = row["mass_center_z"]
        
        print("Bead", index, "at position", x, y, z)
        
        # move PSF in right position in a smaller image
        cle.translate(bead_image_green, single_psf_image, 
                      translate_x= -x + psf_radius,
                      translate_y= -y + psf_radius,
                      translate_z= -z + psf_radius)
    
        # visualize
        # fig, axs = plt.subplots(1,3)    
        # imshow(cle.maximum_x_projection(single_psf_image), plot=axs[0])
        # imshow(cle.maximum_y_projection(single_psf_image), plot=axs[1])
        # imshow(cle.maximum_z_projection(single_psf_image), plot=axs[2])
        
        # average
        avg_psf_image = avg_psf_image + single_psf_image / num_psfs
        
    fig, axs = plt.subplots(1,3)    
    imshow(cle.maximum_x_projection(avg_psf_image), plot=axs[0])
    imshow(cle.maximum_y_projection(avg_psf_image), plot=axs[1])
    imshow(cle.maximum_z_projection(avg_psf_image), plot=axs[2])
    avg_psf_image.min(), avg_psf_image.max()
    normalized_psf = avg_psf_image / np.sum(avg_psf_image)
    
    imshow(normalized_psf, colorbar=True)
    normalized_psf.min(), normalized_psf.max()
    one_micron = 15.4071
    im_max = np.max(avg_psf_image, axis=0)
    im_max = np.asarray(im_max)
    image_line = im_max[20,:]
    image_line_y = im_max[:,20]
    im_line_average = (image_line + image_line_y)/2
    normalizedData = (im_line_average-np.min(im_line_average))/(np.max(im_line_average)-np.min(im_line_average))
    x_max = int(np.floor(len(image_line)/2))
    x_min = x_max * -1
    x_range = np.linspace(x_min, x_max, dtype=int, num=len(im_line_average))
    x_range_microns = x_range/one_micron
    
    fig, axs = plt.subplots()
    points = np.array([x_range_microns, normalizedData]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    norm = plt.Normalize(normalizedData.min(), normalizedData.max())
    lc = LineCollection(segments, cmap='viridis', norm=norm)
    lc.set_array(normalizedData)
    lc.set_linewidth(2)
    
    
    
    plot_line = axs.add_collection(lc)
    plt.ylabel('Relative intensity (A.U.)')
    plt.xlabel('Distance (μm)')
    plt.title('Average lateral PSF λ = 920 nm')
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.text(-1.25,0.78,'n = %s beads' %df.shape[0])
    plt.text(-1.25,0.72,'Objective = fat25x')
    plt.text(-1.25,0.66, 'Zoom = 25x')
    x_min = x_range_microns.min()-0.1
    x_max = x_range_microns.max()+0.1
    axs.set_xlim(x_min, x_max)
    axs.set_ylim(-0.1, 1.1)
    plt.show()
    
    
    from scipy.optimize import curve_fit
    xdata = x_range_microns
    ydata = normalizedData
      
    # Recast xdata and ydata into numpy arrays so we can use their handy features
    xdata = np.asarray(xdata)
    ydata = np.asarray(ydata)
    plt.plot(xdata, ydata, 'o')
      
    # Define the Gaussian function
    def Gauss(x, A, B):
        y = A*np.exp(-1*B*x**2)
        return y
    parameters, covariance = curve_fit(Gauss, xdata, ydata)
      
    fit_A = parameters[0]
    fit_B = parameters[1]
      
    fit_y = Gauss(xdata, fit_A, fit_B)
    plt.plot(xdata, ydata, 'o', label='data')
    plt.plot(xdata, fit_y, '--', label='fit')
    plt.legend()
    
    from scipy.interpolate import UnivariateSpline
    
    # create a spline of x and blue-np.max(blue)/2 
    spline = UnivariateSpline(x_range_microns, fit_y-np.max(fit_y)/2, s=0)
    
    r1, r2 = spline.roots()
    
    import pylab as pl
    
    pl.plot(x_range_microns, fit_y)
    pl.axvspan(r1, r2, facecolor='g', alpha=0.5)
    pl.show()

def get_laser_power():
    """
    Estimate the amount of power emitted at a given laser intensity.
    """

    import numpy as np
    import matplotlib.pyplot as plt

    # data - norm 
    # add option for importing a csv or txt file here
    power_x = np.array([74, 100, 126, 149, 174, 200, 249, 300])
    mW_y = np.array([3.4, 15.2, 33.1, 51.2, 76, 103, 164, 229])

    #find line of best fit
    a, b = np.polyfit(power_x, mW_y, 1)



    plt.scatter(power_x,mW_y, color = 'purple')
    plt.plot(power_x, a*power_x+b, color='steelblue', linestyle='--', linewidth=2)
    plt.xlabel('Laser Power')
    plt.ylabel('mW')
    plt.title('Relationship of laser power to wattage')
    #add fitted regression equation to plot
    plt.text(75, 200, 'y = ' + '{:.2f}'.format(b) + ' + {:.2f}'.format(a) + 'x', size=10)
    plt.text(75, 220, 'Least squares polynomial fit', size=10)
    # Add text about microscope
    # Note to Doug: incorporate this to a file import via XML data.
    plt.text(225, 26, "Wavelength: 920 nm", size=8)
    plt.text(225, 14, "Pockel's bias: 5", size=8)
    plt.text(225, 2, "Objective: fat25x",size=8)
    plt.text(225, -10, "Scan method: resonant", size=8)
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.axis('on')