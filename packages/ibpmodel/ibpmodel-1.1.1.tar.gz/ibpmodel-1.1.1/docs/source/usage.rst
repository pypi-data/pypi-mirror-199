Usage
=====

Calculation of IBP Index
------------------------

To calculate the IBP index use :py:func:`ibpmodel.ibpforward.calculateIBPindex()` function. It returns a pandas.DataFrame:

.. code-block:: python

   >>> from ibpmodel import ibpforward
   >>> ibpforward.calculateIBPindex(day_month=15, longitude=0, local_time=20.9, f107=150)                           
       Doy  Month  Lon    LT  F10.7     IBP
   0   15      1    0  20.9    150  0.4041

  
.. code-block:: python

   >>> ibpforward.calculateIBPindex(day_month=['Jan','Feb','Mar'], local_time=22)
         Doy  Month  Lon  LT  F10.7     IBP
   0     15      1 -180  22    150  0.0851
   1     15      1 -175  22    150  0.0775
   2     15      1 -170  22    150  0.0734
   3     15      1 -165  22    150  0.0749
   4     15      1 -160  22    150  0.0838
   ..   ...    ...  ...  ..    ...     ...
   211   74      3  155  22    150  0.2031
   212   74      3  160  22    150  0.1977
   213   74      3  165  22    150  0.1941
   214   74      3  170  22    150  0.1918
   215   74      3  175  22    150  0.1905
    
   [216 rows x 6 columns]

  
.. code-block:: python

   >>> ibpforward.calculateIBPindex(day_month=[1,15,31], longitude=[-170,175,170], 
      local_time=0, f107=120)
   Doy  Month  Lon  LT  F10.7     IBP
   0    1      1 -170   0    120  0.0301
   1    1      1  175   0    120  0.0397
   2    1      1  170   0    120  0.0437
   3   15      1 -170   0    120  0.0330
   4   15      1  175   0    120  0.0435
   5   15      1  170   0    120  0.0478
   6   31      1 -170   0    120  0.0385
   7   31      1  175   0    120  0.0507
   8   31      1  170   0    120  0.0557

Read coefficient file
---------------------

You can load the coefficient file. :py:func:`ibpmodel.ibpcalc.read_model_file()`:

.. code-block:: python

   >>> from ibpmodel import ibpcalc
   >>> c = ibpcalc.read_model_file()
   >>> c.keys()
   dict_keys(['Parameters', 'Intensity', 'Monthly_LT_Shift', 'Density_Estimators', 
      'Density_Estimator_Lons'])
   >>> c['Intensity']
   array([  -7.09117744,    9.28574894,  118.51795722,   25.55095284,
      -144.4863666 ])




Plotting of the probability
---------------------------

There are two functions to plot IBP index. function :py:func:`ibpmodel.ibpforward.plotIBP()` and :py:func:`ibpmodel.ibpforward.plotButterfly()`.
By default, the plot is displayed immediately. If you want to make changes or additions, the parameter getFig must be set equal to ``True``. 
Then you get matplat.axis as return value:

.. code-block:: python
   
   >>> from ibpmodel import ibpforward
   >>> ibpforward.plotIBPindex(doy=349)

.. image:: _static/example_plotIBP.png
   :alt: Contour plot of the IBP index for the given day
   :align: center
.. code-block:: python

   >>> ibpforward.plotButterflyData(f107=150)

.. image:: _static/example_plotButterfly.png
   :alt: Contour plot of result from function ButterflyData() 
   :align: center

.. code-block:: python
   
   >>> import matplotlib.pyplot as plt
   >>> ax=ibpforward.plotIBPindex(310,getFig=True)
   >>> plt.show()


