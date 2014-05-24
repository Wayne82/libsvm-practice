//
//  SignalDistancePredictor.cpp
//
//  Created by waynewang on 21/5/14.
//  Copyright (c) 2014 waynewang. All rights reserved.
//
#include <SignalDistancePredictor.h>
#include <SignalDistanceLibSvm.h>
#include <SignalDistanceLModel.h>

SignalDistancePredictor::SignalDistancePredictor()
   : m_signals_dim(0)
   , m_signals_count(0)
   , m_model(nullptr)
{
   
}

SignalDistancePredictor::~SignalDistancePredictor()
{
   if (m_model != nullptr)
   {
      m_model->UnRef();
      m_model = nullptr;
   }
}

void 
SignalDistancePredictor::SetLearnModel(SignalDistanceLModel* model)
{
   if (m_model == model)
      return;

   if (m_model != nullptr)
      m_model->UnRef();

   m_model = model;

   if (m_model)
      m_model->Ref();

   // Then, initialize predictor as the learn model is setup or changed.
   Init();
}

void 
SignalDistancePredictor::Init()
{
   // m_model should never be null at this moment.
   m_signals_count = 0;
   m_signals_dim = m_model->GetSignalsDimension();
   m_signals.reserve(m_signals_dim);
}

bool
SignalDistancePredictor::Predict(double signal, double* dist, double* precision)
{
   bool success = false;

   // If haven't set up learn model, or the learn model is not valid,
   // then return earlier.
   if (m_model == nullptr || 
      m_model->GetSvmModel() == nullptr)
      return success;

   if (dist == nullptr)
      return success;

   if (m_signals_count < m_signals_dim)
   {
      // Can't predict if the given samples are less than the feature space.
      m_signals[m_signals_count] = signal;
      *dist = 0.0;
   }
   else 
   {
      // Push new signal and pop the oldest one.
      if (m_signals_count > m_signals_dim)
      {
         for (unsigned int i=0; i<m_signals_dim-1; ++i)
            m_signals[i] = m_signals[i+1];
         m_signals[m_signals_dim-1] = signal;
      }

      // Construct svm node, m_cur_node shouldn't be nullptr.
      svm_node* nodes = m_model->GetSignalsNodes();
      for (unsigned int i=0; i<m_signals_dim; ++i)
      {
         nodes[i].index = i+1;
         nodes[i].value = m_signals[i];
      }

      // TODO: need to scale before prediction, using the same scale range of 
      // the training model.

      // Do predict
      double predict_label = svm_predict(m_model->GetSvmModel(), nodes);
      
      *dist = predict_label;
      success = true;
   }
   m_signals_count++;
   
   return success;
}
