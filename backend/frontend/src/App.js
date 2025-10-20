import React from 'react';

function App() {
  return React.createElement('div', { 
    style: { 
      padding: '50px', 
      textAlign: 'center',
      backgroundColor: '#f0f8ff',
      minHeight: '100vh'
    }
  }, 
  React.createElement('h1', null, 'AI App Builder'),
  React.createElement('p', null, 'Frontend is working!')
  );
}

export default App;
