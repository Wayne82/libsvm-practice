//
//  SignalDistanceLModel.h
//
//  Created by waynewang on 24/5/14.
//  Copyright (c) 2014 waynewang. All rights reserved.
//
#include <SignalDistanceLModel.h>
#include <SignalDistanceLibSvm.h>

SignalDistanceLModel::SignalDistanceLModel(const char* model_path, const char *scale_range_path)
   : m_model(nullptr)
   , m_nodes(nullptr)
   , m_model_path(new std::string(model_path))
   , m_scale_range_path(new std::string(scale_range_path))
   , m_ref_count(0)
{
   // Load learn model.
   m_model = svm_load_model(model_path);

   // Get scale range for scaling samples.
   ExtractScaleRange();

   // Initialize svm node for a sample
   m_nodes = new svm_node[FEATURE_SPACE+1];
   m_nodes[FEATURE_SPACE].index = -1;
}

SignalDistanceLModel::~SignalDistanceLModel()
{
   if (m_model != nullptr)
      svm_free_and_destroy_model(&m_model);

   delete []m_nodes;
   m_nodes = nullptr;

   delete m_model_path;
   m_model_path = nullptr;
   delete m_scale_range_path;
   m_scale_range_path = nullptr;
}

int 
SignalDistanceLModel::GetSvmModelType() const
{
   if (m_model != nullptr)
      return svm_get_svm_type(m_model);

   return -1;
}

bool 
SignalDistanceLModel::IsValidScaleRange() const
{
   return m_feature_min.size() > 0 && m_feature_max.size() > 0;
}

void 
SignalDistanceLModel::ExtractScaleRange()
{
   // TO IMPLEMENT:

}

double 
SignalDistanceLModel::ScaleAttributeAtIndex(double attri, unsigned int index)
{
   // TO IMPLEMENT:
   return attri;
}