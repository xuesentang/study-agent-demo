import { useState } from 'react';
import { StudyMode } from './components/StudyMode';
import  ChatMode  from './components/ChatMode';
import type { AppMode } from './types';
import './App.css';

function App() {
  const [mode, setMode] = useState<AppMode>('study');
  const [sessionId] = useState(() => 'session_' + Date.now());
  
  return (
    <div className="app">
      {mode === 'study' ? (
        <StudyMode 
          sessionId={sessionId}
          onSwitchMode={() => setMode('chat')}
        />
      ) : (
        <ChatMode 
          sessionId={sessionId}
          onSwitchMode={() => setMode('study')}
        />
      )}
    </div>
  );
}

export default App;