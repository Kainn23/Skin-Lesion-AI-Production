import React from 'react';
import { Upload, Settings, Cpu, FileSearch, Layers, Stethoscope, ChevronRight } from 'lucide-react';

export default function PipelineVisualization({ isAnalyzing, step }) {
  // step: 0 = idle, 1 = preprocessing, 2 = inference, 3 = explainability, 4 = complete
  
  const steps = [
    { id: 1, label: 'Upload Image', icon: Upload },
    { id: 2, label: 'Preprocessing', icon: Settings },
    { id: 3, label: 'EfficientNet-B0', icon: Cpu },
    { id: 4, label: 'Prediction', icon: FileSearch },
    { id: 5, label: 'GradCAM', icon: Layers },
    { id: 6, label: 'Clinical Output', icon: Stethoscope },
  ];

  // Determine active step based on state
  let activeStep = 0;
  if (step === 4) activeStep = 6;
  else if (isAnalyzing) activeStep = 3; // mock active state

  return (
    <div className="mb-8">
      <div className="flex items-center justify-between overflow-x-auto custom-scrollbar py-2 px-1">
        {steps.map((s, i) => {
          const isActive = activeStep === s.id || (isAnalyzing && s.id <= 3);
          const isCompleted = activeStep > s.id;
          
          return (
            <React.Fragment key={s.id}>
              <div className="flex flex-col items-center gap-2 min-w-[80px]">
                <div 
                  className={`w-12 h-12 rounded-2xl flex items-center justify-center transition-all duration-500
                    ${isActive ? 'bg-primary text-white shadow-lg shadow-primary/30 scale-110' : 
                      isCompleted ? 'bg-primary/20 text-primary' : 
                      'bg-slate-100 dark:bg-slate-800 text-slate-400'}
                  `}
                >
                  <s.icon size={20} className={isActive && isAnalyzing && s.id === 3 ? 'animate-pulse' : ''} />
                </div>
                <span className={`text-[10px] font-bold uppercase tracking-wider text-center ${isActive ? 'text-primary' : 'text-text-color opacity-50'}`}>
                  {s.label}
                </span>
              </div>
              
              {i < steps.length - 1 && (
                <div className="flex-1 min-w-[20px] max-w-[40px] flex items-center justify-center">
                  <ChevronRight size={16} className={isCompleted || isActive ? 'text-primary' : 'text-slate-300 dark:text-slate-700'} />
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
}
