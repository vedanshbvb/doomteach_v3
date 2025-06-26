import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useNavigate
} from 'react-router-dom';

function OAuthSuccess() {
  const navigate = useNavigate();
  return (
    <div className="app">
      <h1 className="title">doomteach</h1>
      <div className="subtitle">Signed in successfully!</div>
      <button
        className="prompt-form-button"
        style={{ marginTop: '2rem' }}
        onClick={() => navigate('/')}
      >
        Go to Homepage
      </button>
    </div>
  );
}

function App() {
  const [prompt, setPrompt] = useState('');
  const [status, setStatus] = useState('');
  const [videoGenerated, setVideoGenerated] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploaded, setUploaded] = useState(false);
  const [videoId, setVideoId] = useState(null);

  // Check if redirected from OAuth and trigger upload
  useEffect(() => {
    if (window.location.pathname === '/' && window.location.hash === '#upload') {
      setUploading(true);
      axios.post('/api/upload-video')
        .then(res => {
          setUploading(false);
          setUploaded(true);
          setVideoId(res.data.videoId);
        })
        .catch(() => {
          setUploading(false);
          setStatus('Video upload failed.');
        });
      // Remove hash from URL
      window.history.replaceState(null, '', '/');
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('Generating...');
    setVideoGenerated(false);
    try {
      const res = await axios.post('http://localhost:5000/api/generate', { prompt });
      setStatus('');
      setVideoGenerated(true);
    } catch (err) {
      setStatus('Error generating video.');
    }
  };

  const handlePostToYouTube = (e) => {
    e.preventDefault();
    // Redirect to Google OAuth, and after OAuth, redirect back to /#upload
    window.location.href = 'http://localhost:5000/api/auth/google?redirect=/#upload';
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={
          <div className="app">
            <h1 className="title">doomteach</h1>
            <div className="subtitle">Your viral video is just a prompt away</div>
            <form onSubmit={handleSubmit} className="prompt-form">
              <input
                type="text"
                placeholder="Enter your prompt..."
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
              />
              <button type="submit">Send</button>
            </form>
            {status === 'Generating...' && (
              <div className="generating-text">Generating...</div>
            )}
            {videoGenerated && (
              <>
                <div className="video-generated-text">
                  Video generated at <span className="video-path">doomteach/media/generated/video/doom_video_with_subs.mp4</span>
                </div>
                <video width="480" height="270" controls style={{ marginTop: '16px' }}>
                  <source src="http://localhost:5000/media/video/doom_video_with_subs.mp4" type="video/mp4" />
                  Your browser does not support the video tag.
                </video>
                <div style={{ marginTop: '16px' }}>
                  <button onClick={handlePostToYouTube} disabled={uploading}>
                    {uploading ? 'Uploading to YouTube...' : 'Post to YouTube'}
                  </button>
                </div>
                {uploaded && videoId && (
                  <div className="video-generated-text" style={{ color: '#00fff7' }}>
                    Uploaded! View on <a href={`https://youtube.com/watch?v=${videoId}`} target="_blank" rel="noopener noreferrer">YouTube</a>.
                  </div>
                )}
                {status === 'Video upload failed.' && (
                  <div className="video-generated-text" style={{ color: 'red' }}>{status}</div>
                )}
              </>
            )}
          </div>
        } />
        <Route path="/oauth-success" element={<OAuthSuccess />} />
      </Routes>
    </Router>
  );
}

export default App;
