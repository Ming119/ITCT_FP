import { Container, Row, Col, Button } from 'react-bootstrap';
import { useState } from 'react';

export const App = () => {
  const [input, setInput] = useState('');

  const onSubmitClick = async () => {
    console.log(input);
    const response = await fetch('http://localhost:8000/send', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message: input })  
    });
  }

  const renderOutput = () => {
  
  };

  return (
    <Container>
      <h1>ITCT Final Project</h1>
      <hr />

      <Row>
        <Col className="border-right">
          <h2>Input:</h2>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            rows={10}
            cols={50}
          />
          <br />
          <Button onClick={ onSubmitClick }>Submit</Button>
        </Col>

        <Col className="border-left">
          <h2>Output:</h2>
          { renderOutput() }
        </Col>
      </Row>
    </Container>
  )
};

export default App;