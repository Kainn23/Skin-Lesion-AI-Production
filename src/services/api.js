export const analyzeLesion = async (imageFile) => {
  const formData = new FormData();
  formData.append('file', imageFile);

  try {
    const response = await fetch('/api/predict', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      let errorMessage = 'Failed to analyze lesion';
      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorMessage;
      } catch (e) {
        const text = await response.text();
        if (text) errorMessage = text;
      }
      
      if (response.status === 502 || response.status === 504 || errorMessage.includes('ECONNREFUSED')) {
        errorMessage = 'Backend server is unreachable. Please ensure FastAPI is running on port 8000.';
      }
      
      throw new Error(errorMessage);
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

export const generateGradCAM = async (imageFile) => {
  const formData = new FormData();
  formData.append('file', imageFile);

  try {
    const response = await fetch('/api/gradcam', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      let errorMessage = 'Failed to generate GradCAM';
      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorMessage;
      } catch (e) {
        const text = await response.text();
        if (text) errorMessage = text;
      }
      
      if (response.status === 502 || response.status === 504 || errorMessage.includes('ECONNREFUSED')) {
        errorMessage = 'Backend server is unreachable. Please ensure FastAPI is running on port 8000.';
      }
      
      throw new Error(errorMessage);
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

export const getRandomExamples = async (count = 8) => {
  try {
    const response = await fetch(`/api/examples/random?count=${count}`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch examples');
    }
    
    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};
