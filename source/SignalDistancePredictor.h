//
//  SignalDistancePredictor.h
//
//  Created by waynewang on 21/5/14.
//  Copyright (c) 2014 waynewang. All rights reserved.
//
#ifndef _SIGNALDISTANCEPREDICTOR_HDR_
#define _SIGNALDISTANCEPREDICTOR_HDR_

#include <SignalDistancePublic.h>

// Now directly use svm c structures, interfaces here.
// Later, better to wrapper them in a c++ class.

// Forward struct
struct svm_model;
struct svm_node;

class EXPORT_API SignalDistancePredictor
{
public:
   enum { FEATURE_SPACE = 10 };
   enum PredictModel 
   {
      ePREDICT_CLASSIFICATION = 0,
      ePREDICT_REGRESSION = 1,

      ePREDICT_MODEL_COUNT
   };

   SignalDistancePredictor(PredictModel model);
   ~SignalDistancePredictor();
   
   // Do predict
   // signal, is the input value
   // dist, is the predicted distance
   // precision, is the precision of the predict (currently now used)
   // return true, if successfully get a prediction, otherwise false.
   bool Predict(double signal, double* dist, double* precision);

   // Explicitly set the path to the trained models.
   static void SetModelsPath(const char* models_path);

private:
   // Do not allow copy and assignment
   SignalDistancePredictor(const SignalDistancePredictor& other);
   SignalDistancePredictor& operator=(const SignalDistancePredictor& other);

   // Initalize the svm model, which can be used for all following predictions.
   bool Init(PredictModel model);
   // Terminate, and clean up.
   void Term();

private:
   double m_signals[FEATURE_SPACE];
   unsigned int m_count; 

   svm_model* m_model;
   svm_node* m_cur_node;

   static const char* m_models_path;
};

#endif // _SIGNALDISTANCEPREDICTOR_HDR_