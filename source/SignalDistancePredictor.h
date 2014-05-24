//
//  SignalDistancePredictor.h
//
//  Created by waynewang on 21/5/14.
//  Copyright (c) 2014 waynewang. All rights reserved.
//
#ifndef _SIGNALDISTANCEPREDICTOR_HDR_
#define _SIGNALDISTANCEPREDICTOR_HDR_

#include <SignalDistancePublic.h>
#include <vector>

// Now directly use svm c structures, interfaces here.
// Later, better to wrapper them in a c++ class.

// Forward declaration
class SignalDistanceLModel;

EXPORT_TEMPLATE(std::vector<double>, SignalsVec);

class EXPORT_API SignalDistancePredictor
{
public:

   SignalDistancePredictor();
   ~SignalDistancePredictor();
   
   // Set learn model
   void SetLearnModel(SignalDistanceLModel* model);

   /**
   // Do predict
   //
   // @param signal is the input value
   // @param dist is the predicted distance
   // @param precision is the precision of the predict (currently now used)
   // @return true if successfully get a prediction, otherwise false.
   */
   bool Predict(double signal, double* dist, double* precision);

private:
   // Do not allow copy and assignment
   SignalDistancePredictor(const SignalDistancePredictor& other);
   SignalDistancePredictor& operator=(const SignalDistancePredictor& other);

   // Initialize predictor
   void Init();

private:
   SignalsVec m_signals;
   unsigned int m_signals_dim;
   unsigned int m_signals_count; 

   SignalDistanceLModel* m_model;
};

#endif // _SIGNALDISTANCEPREDICTOR_HDR_