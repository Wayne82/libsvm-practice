//
//  SignalDistanceLModel.h
//
//  Created by waynewang on 24/5/14.
//  Copyright (c) 2014 waynewang. All rights reserved.
//
#include <SignalDistanceLModel.h>
#include <SignalDistanceLibSvm.h>

SignalDistanceLModel::SignalDistanceLModel(const char* model_path)
   : m_model(nullptr)
   , m_nodes(nullptr)
   , m_ref_count(0)
{
   m_model = svm_load_model(model_path);
   m_nodes = new svm_node[FEATURE_SPACE_DIM+1];
   m_nodes[FEATURE_SPACE_DIM].index = -1;
}

SignalDistanceLModel::~SignalDistanceLModel()
{
   if (m_model != nullptr)
      svm_free_and_destroy_model(&m_model);

   if (m_nodes != nullptr)
   {
      delete []m_nodes;
      m_nodes = nullptr;
   }
}

int 
SignalDistanceLModel::GetSvmModelType() const
{
   if (m_model != nullptr)
      return svm_get_svm_type(m_model);

   return -1;
}
