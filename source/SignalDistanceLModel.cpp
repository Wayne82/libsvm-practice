//
//  SignalDistanceLModel.h
//
//  Created by waynewang on 24/5/14.
//  Copyright (c) 2014 waynewang. All rights reserved.
//
#include <SignalDistanceLModel.h>
#include <SignalDistanceLibSvm.h>

// File handle helper class
class FileHandle
{
public:
   enum { DEFAULT_LINE_LENGTH = 1024 };

   FileHandle(const char* file_name)
      : m_fp(nullptr)
   {
      errno_t err = fopen_s(&m_fp, file_name, "r");
      (void)(err);
      m_line.reserve(DEFAULT_LINE_LENGTH);
   }
   ~FileHandle()
   {
      fclose(m_fp);
   }

   bool IsValid() const 
   { return m_fp != nullptr; }

   FILE* GetFileHandle()
   { return m_fp; }

   const char* ReadLine()
   {
      size_t cap = m_line.capacity();
      if (fgets( const_cast<char*>(m_line.c_str()), static_cast<int>(cap), m_fp) == nullptr)
         return nullptr;

      // Line is longer than 1024 chars.
      while (strrchr(m_line.c_str(), '\n') == nullptr)
      {
         cap <<= 1;
         m_line.reserve(cap);
         size_t len = m_line.length();
         if (fgets(const_cast<char*>(m_line.c_str())+len, static_cast<int>(cap-len), m_fp) == nullptr)
            break;
      }

      return m_line.c_str();
   }

   void Rewind()
   {
      rewind(m_fp);
   }

private:
   // Do not allow copy and assignment.
   FileHandle(const FileHandle& other);
   FileHandle& operator=(const FileHandle& other);

   typedef std::string LINE;

private:
   FILE* m_fp;
   LINE m_line;
};

SignalDistanceLModel::SignalDistanceLModel(const char* model_path, const char *scale_range_path)
   : m_model(nullptr)
   , m_nodes(nullptr)
   , m_model_path(new std::string(model_path))
   , m_scale_range_path(new std::string(scale_range_path))
   , m_feature_space_size(0)
   , m_ref_count(0)
{
   // Load learn model.
   m_model = svm_load_model(model_path);

   // Get scale range for scaling samples.
   ExtractScaleRange();

   // Initialize svm node for a sample
   m_nodes = new svm_node[m_feature_space_size+1];
   m_nodes[m_feature_space_size].index = -1;
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
   m_feature_min.clear();
   m_feature_max.clear();

   // In theory scale range path should always exist
   if (m_scale_range_path == nullptr)
      return; 

   FileHandle scale_file(m_scale_range_path->c_str());
   // If not valid, return directly.
   if (!scale_file.IsValid())
      return;

   const char* line = scale_file.ReadLine();
   if (line == nullptr)
      return;

   // Assume the scale file only scale attributes, not target label.
   if (line[0] == 'x')
   {
      scale_file.ReadLine();
   }
   else 
   {
      return;
   }

   // Get max index, we assume its equal to feature space size.
   int max_index = 0;
   int cur_index = 0;
   line = scale_file.ReadLine();
   while (line != nullptr && 
          sscanf_s(line, "%d %*f %*f\n", &cur_index) == 1)
   {
      max_index = libsvm_max(max_index, cur_index);
      line = scale_file.ReadLine();
   }
   scale_file.Rewind();
   m_feature_max.reserve(max_index+1);
   m_feature_min.reserve(max_index+1);

   // Read data
   scale_file.ReadLine(); // Read x.
   scale_file.ReadLine(); // Read x lower, upper value.
   line = scale_file.ReadLine(); // Read min, max value for each index.
   double fmin, fmax;
   while (line != nullptr && 
          sscanf_s(line, "%d %1f %1f", &cur_index, &fmin, &fmax) == 3)
   {
      m_feature_max[cur_index] = fmax;
      m_feature_min[cur_index] = fmin;
      line = scale_file.ReadLine();
   }

}

double 
SignalDistanceLModel::ScaleAttributeAtIndex(double attri, unsigned int index)
{
   // TO IMPLEMENT:
   return attri;
}