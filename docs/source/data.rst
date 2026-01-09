====================
Data
====================
--------------------

.. currentmodule:: musicnpy.data

Introduction
===================
This module provide a collection of models available in the library for different types of musical data.

|

PMod Class
===================

PMod is a class for handling pitch models in musical data.

.. code-block:: python
   
   from musicnpy.data import PMod

   print(PMod.maj)
   >>> {
         'intervals': [0, 2, 4, 5, 7, 9, 11], 
         'scale_harmo': ['maj', 'min', 'min', 'maj', 'maj', 'min', 'dim'], 
         'chord': [0, 4, 7]
       }