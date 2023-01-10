import { useEffect, useState } from "react";
import React from 'react';
import { Navbar,Container,Nav} from "react-bootstrap";
import logo from '../assets/img/logo.svg';
import navIcon1 from '../assets/img/nav-icon1.svg';
import navIcon2 from '../assets/img/nav-icon2.svg';
import navIcon3 from '../assets/img/nav-icon3.svg';
 
export const NavBar = () =>{
    const [activeLink, setActiveLink] = useState('home');
    const [scrolled, seScrolled] = useState(false);

    useEffect(() => {
        const onScroll = () =>{
            if (window.scrollY > 50) {
                seScrolled(true);
            }else{
                seScrolled(false);
            }
        }
        window.addEventListener('scroll',onScroll);

        return () => window.removeEventListener('scroll',onScroll);
    },[])

    const onUpdateActiveLink = (value) =>{
        setActiveLink(value);
    }

    return (
        <Navbar bg="primary" expand="lg" className={scrolled? 'scrolled':''}>  
        <Container>  
            <img src={logo} alt="Logo"/>
        <Navbar.Brand href="#home">
        </Navbar.Brand>  
        <Navbar.Toggle aria-controls="basic-navbar-nav">
         <span className='navbar-toggler-icon'></span>
        </Navbar.Toggle>  
        <Navbar.Collapse id="basic-navbar-nav">  
            <Nav className="me-auto">  
            <Nav.Link href="#home" className={activeLink === 'home'?'active navbar-link':'navbar-link'} onClick={() => onUpdateActiveLink('home')}>Home</Nav.Link>  
            <Nav.Link href="#competences" className={activeLink === 'competences'?'active navbar-link':'navbar-link'} onClick={() => onUpdateActiveLink('competences')}>Competences</Nav.Link> 
            <Nav.Link href="#skills" className={activeLink === 'skills'?'active navbar-link':'navbar-link'} onClick={() => onUpdateActiveLink('skills')}>Skills</Nav.Link>
            <Nav.Link href="#expertise" className={activeLink === 'expertise'?'active navbar-link':'navbar-link'} onClick={() => onUpdateActiveLink('expertise')}>Expertises</Nav.Link> 
            </Nav>  
            <span className='navbar-text'>
             <div className="social-icon">
               <a href='#'><img src={navIcon1} alt=""/> </a> 
               <a href='#'><img src={navIcon2} alt=""/> </a> 
               <a href='#'><img src={navIcon3} alt=""/> </a> 
             </div>  
                <button className="lmbtn" onClick={()=> console.log('connect')}><span>MMJJ</span> </button> 
            </span>      
        </Navbar.Collapse>  
        </Container>  
      </Navbar>  
    )
}