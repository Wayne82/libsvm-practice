//
//  SignalDistanceLModel.h
//
//  Created by waynewang on 24/5/14.
//  Copyright (c) 2014 waynewang. All rights reserved.
//
#ifndef _SIGNALDISTANCELMODEL_HDR_
#define _SIGNALDISTANCELMODEL_HDR_

#include <SignalDistancePublic.h>

// Forward declaration
struct svm_model;
struct svm_node;

class EXPORT_API SignalDistanceLModel
{
public:
   SignalDistanceLModel(const char* model_path);

   // Assume the learn model is trained from the samples of 10 dimension space.
   // ??? Need to get the dimension from the learn model automatically.
   // ??? But seems libsvm doesn't retain such information, need to figure out other ways.
   enum { FEATURE_SPACE_DIM = 10 };

   // Interfaces to access status of the model
   int GetSvmModelType() const;

   const svm_model* GetSvmModel() const 
   { return m_model; }
   unsigned int GetSignalsDimension() const
   { return FEATURE_SPACE_DIM; }
   svm_node* GetSignalsNodes() const
   { return m_nodes; }

   // Ref count manage, learn model can be shared between 
   // different predictors.
   void Ref()
   {
      ++ m_ref_count;
   }

   void UnRef()
   {
      if (m_ref_count > 1)
         -- m_ref_count;
      else 
         delete this;
   }

   unsigned int RefCount() const 
   { return m_ref_count; }

protected:
   ~SignalDistanceLModel();

private:
   // Do not allow copy and assignment
   SignalDistanceLModel(const SignalDistanceLModel& other);
   SignalDistanceLModel& operator=(const SignalDistanceLModel& other);

private:
   svm_model* m_model;
   svm_node* m_nodes;

   unsigned int m_ref_count;
};

#endif // _SIGNALDISTANCELMODEL_HDR_