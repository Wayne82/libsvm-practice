//
//  SignalDistancePredictor.cpp
//
//  Created by waynewang on 21/5/14.
//  Copyright (c) 2014 waynewang. All rights reserved.
//
#include <SignalDistancePredictor.h>
#include <SignalDistanceLibSvm.h>
#include <string>

const char* MODEL_NAME[SignalDistancePredictor::ePREDICT_MODEL_COUNT] = {
   "signal_distance_classification.model",
   "signal_distance_regression.model"
};

const char* SignalDistancePredictor::m_models_path = nullptr;

SignalDistancePredictor::SignalDistancePredictor(PredictModel model)
{
   Init(model);
}

SignalDistancePredictor::~SignalDistancePredictor()
{
   Term();
}

void 
SignalDistancePredictor::SetModelsPath(const char* models_path)
{
   m_models_path = models_path;
}

bool
SignalDistancePredictor::Init(PredictModel model)
{
   if (m_models_path == nullptr)
      return false;

   m_count = 0;
   m_model = nullptr;
   m_cur_node = nullptr;
   memset(m_signals, 0, sizeof(double)*FEATURE_SPACE);

   char name[1024];
   strcpy_s(name, m_models_path);
   strcat_s(name, MODEL_NAME[model]);
   m_model = svm_load_model(name);
   m_cur_node = new svm_node[FEATURE_SPACE+1];

   return m_model != nullptr;
}

void 
SignalDistancePredictor::Term()
{
   svm_free_and_destroy_model(&m_model);
   delete []m_cur_node;
   m_cur_node = nullptr;
}

bool
SignalDistancePredictor::Predict(double signal, double* dist, double* precision)
{
   if (dist == nullptr)
      return false;

   if (m_count < FEATURE_SPACE)
   {
      // Can't predict if the given samples are less than the feature space.
      m_signals[m_count] = signal;
      m_count++;
      *dist = 0.0;
      return false;
   }
   else 
   {
      // Push new signal and pop the oldest one.
      if (m_count > FEATURE_SPACE)
      {
         for (int i=0; i<FEATURE_SPACE-1; ++i)
            m_signals[i] = m_signals[i+1];
         m_signals[FEATURE_SPACE-1] = signal;
      }

      // Construct svm node, m_cur_node shouldn't be nullptr.
      for (int i=0; i<FEATURE_SPACE; ++i)
      {
         m_cur_node[i].index = i+1;
         m_cur_node[i].value = m_signals[i];
      }
      m_cur_node[FEATURE_SPACE].index = -1;

      // TODO: need to scale before prediction, using the same scale range of 
      // the training model.

      // Do predict
      double predict_label = svm_predict(m_model, m_cur_node);
      
      *dist = predict_label;
      return true;
   }
}
