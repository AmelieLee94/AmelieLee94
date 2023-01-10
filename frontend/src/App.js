import logo from './logo.svg';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import { NavBar } from './components/NavBar';

function App() {
  return (
    <div className="App">
       {/* <NavBar bg="primary" expand="md">  
    <Container>  
      <NavBar.Brand href="#home">Navbar Brand</NavBar.Brand>  
      <NavBar.Toggle aria-controls="basic-navbar-nav"/>  
      <NavBar.Collapse id="basic-navbar-nav">  
        <Nav className="me-auto">  
          <Nav.Link href="#home">Home</Nav.Link>  
          <Nav.Link href="#link">Link</Nav.Link>  
        </Nav>  
      </NavBar.Collapse>  
    </Container>  
  </NavBar>   */}
  <NavBar/>
    </div>
  );
}

export default App;
