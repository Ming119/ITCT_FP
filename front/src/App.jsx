import { Container, Row, Col, Button } from 'react-bootstrap';
import { useEffect, useState } from 'react';

export const App = () => {
  const [input, setInput] = useState('');
  const [output, setOutput] = useState('');
  const [bps, setBps] = useState(0);
  const [isFinished, setIsFinished] = useState(false);

  const onSubmitClick = async () => {
    const response = await fetch('http://localhost:8001/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: input })  
    });
    if (response.status === 200)
      setIsFinished(true);
  }

  useEffect(() => {
    let failuresCount = 0;
    if (isFinished) {
      const interval = setInterval(async () => {
        const response = await fetch('http://localhost:8002/get_result', {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' }
        });
        if (response.status === 200) {
          const data = await response.json();
          if (data.message === "" && data.bps === 0) {
            failuresCount++;
            if (failuresCount >= 5) {
              clearInterval(interval);
              setIsFinished(false);
              setOutput("Error: Server is not responding");
            }
            return;
          }
          setOutput(data.message);
          setBps(data.bps);
          setIsFinished(false);
        }
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [isFinished]);

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
          { output }
          <br /><br />
          { bps } bit/s
        </Col>
      </Row>
    </Container>
  )
};

export default App;
