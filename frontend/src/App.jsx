import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import ExampleGallery from './components/ExampleGallery';
import UploadArea from './components/UploadArea';
import PipelineVisualization from './components/PipelineVisualization';
import PredictionCard from './components/PredictionCard';
import DifferentialDiagnosis from './components/DifferentialDiagnosis';
import ImagePreview from './components/ImagePreview';
import GradCAMViewer from './components/GradCAMViewer';
import LesionInfoPanel from './components/LesionInfoPanel';
import ABCDEAssessment from './components/ABCDEAssessment';
import ModelInfo from './components/ModelInfo';
import HistoryPanel from './components/HistoryPanel';
import { analyzeLesion, generateGradCAM } from './services/api';

export default function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [pipelineStep, setPipelineStep] = useState(0);
  
  const [predictionData, setPredictionData] = useState(null);
  const [gradcamData, setGradcamData] = useState(null);
  const [error, setError] = useState(null);

  const [history, setHistory] = useState([]);

  // Load history on mount
  useEffect(() => {
    const saved = localStorage.getItem('lesion_history');
    if (saved) {
      try {
        setHistory(JSON.parse(saved));
      } catch (e) {
        console.error("Error parsing history", e);
      }
    }
  }, []);

  const handleFileSelect = async (file) => {
    setSelectedFile(file);
    const objectUrl = URL.createObjectURL(file);
    setPreviewUrl(objectUrl);
    
    // Reset state
    setPredictionData(null);
    setGradcamData(null);
    setError(null);
    
    setIsAnalyzing(true);
    setPipelineStep(1); // Preprocessing

    try {
      setPipelineStep(2); // EfficientNet / Prediction
      const result = await analyzeLesion(file);
      setPredictionData(result);
      
      setPipelineStep(3); // GradCAM
      const gradcamResult = await generateGradCAM(file);
      setGradcamData(gradcamResult);
      
      setPipelineStep(4); // Complete
      
      // Save to history
      const historyItem = {
        timestamp: new Date().toISOString(),
        prediction: result.prediction,
        confidence: result.confidence,
        imageUrl: objectUrl,
      };
      
      const newHistory = [historyItem, ...history].slice(0, 10); // Keep last 10
      setHistory(newHistory);
      localStorage.setItem('lesion_history', JSON.stringify(newHistory));
      
    } catch (err) {
      setError(err.message);
      setPipelineStep(0);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleSelectHistory = (item) => {
    // In a real app we'd load the full object, but here we just reset for demo
    setPreviewUrl(item.imageUrl);
    // Mock the state (we don't have the full probabilities or gradcam from history easily without storing it all)
    // A robust implementation would store the full API response in history.
    setPredictionData({
      prediction: item.prediction,
      confidence: item.confidence,
      probabilities: { [item.prediction]: item.confidence },
      abcde: null
    });
    setGradcamData(null);
    setPipelineStep(4);
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <Header />
      
      <main>
        <ExampleGallery onSelectExample={(url) => {
          fetch(url).then(r => r.blob()).then(blob => {
            const file = new File([blob], "example.jpg", { type: "image/jpeg" });
            handleFileSelect(file);
          });
        }} />
        
        <UploadArea 
          onFileSelect={handleFileSelect} 
          selectedFile={selectedFile} 
          previewUrl={previewUrl} 
          isAnalyzing={isAnalyzing} 
        />
        
        {(isAnalyzing || predictionData) && (
          <PipelineVisualization isAnalyzing={isAnalyzing} step={pipelineStep} />
        )}
        
        {error && (
          <div className="mb-8 p-4 bg-red-50 dark:bg-red-500/10 text-red-600 border border-red-200 dark:border-red-500/20 rounded-2xl font-medium">
            Error: {error}
          </div>
        )}

        {(predictionData || isAnalyzing) && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 mb-8">
            
            {/* Left Column */}
            <div className="lg:col-span-5 flex flex-col gap-6">
              <ImagePreview imageUrl={previewUrl} />
              
              {predictionData && (
                <>
                  <PredictionCard 
                    prediction={predictionData.prediction} 
                    confidence={predictionData.confidence} 
                  />
                  <DifferentialDiagnosis probabilities={predictionData.probabilities} />
                </>
              )}
            </div>
            
            {/* Right Column */}
            <div className="lg:col-span-7 flex flex-col gap-6">
              <LesionInfoPanel prediction={predictionData?.prediction} />
              
              <GradCAMViewer 
                originalImage={previewUrl} 
                gradcamImage={gradcamData ? `/api/${gradcamData.gradcam_path.replace(/\\/g, '/')}` : null} 
              />
              
              {predictionData?.abcde && (
                <ABCDEAssessment data={predictionData.abcde} />
              )}
            </div>

          </div>
        )}

        <HistoryPanel history={history} onSelectHistory={handleSelectHistory} />
        
        <ModelInfo />
      </main>
    </div>
  );
}
