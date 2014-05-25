//
//  SignalDistanceLModel.h
//
//  Created by waynewang on 24/5/14.
//  Copyright (c) 2014 waynewang. All rights reserved.
//
#ifndef _SIGNALDISTANCELMODEL_HDR_
#define _SIGNALDISTANCELMODEL_HDR_

#include <SignalDistancePublic.h>
#include <string>

// Forward declaration
struct svm_model;
struct svm_node;

EXPORT_TEMPLATE(std::vector<double>, FeatureVec);

class EXPORT_API SignalDistanceLModel
{
public:
   SignalDistanceLModel(const char *model_path, const char *scale_range_path);

   // Interfaces to access status of the model
   int GetSvmModelType() const;
   const svm_model* GetSvmModel() const 
   { return m_model; }
   unsigned int GetSvmFeatureSpace() const
   { return m_feature_space_size; }
   svm_node* GetSvmNodes() const
   { return m_nodes; }
   bool IsValidModel() const
   { return m_model != nullptr && m_feature_space_size != 0; }

   // Scale a attribute at given index
   double ScaleAttributeAtIndex(double attri, unsigned int index);

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

   // Extracting scale range, which is used by the learn model
   // we need them to scale samples before predicting.
   bool ExtractScaleRange();

private:
   svm_model *m_model;
   svm_node *m_nodes;

   // model file path and scale range file path
   std::string *m_model_path;
   std::string *m_scale_range_path;

   // scale range for each feature
   FeatureVec m_feature_min;
   FeatureVec m_feature_max;
   double m_feature_lower;
   double m_feature_upper;
   unsigned int m_feature_space_size;
   
   unsigned int m_ref_count;
};

#endif // _SIGNALDISTANCELMODEL_HDR_