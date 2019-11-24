import React, { Component } from 'react';
import {Box,Paper, Button,Typography,Input} from '@material-ui/core';
import {store} from './../../App';
import {sendLogin} from './../Actions/LoginVer'
export function isLogged(){
  store.dispatch(sendLogin());
  return 1;
}


class Login extends Component {

  render(){
    return (
      <div style={{margin:'10% 30%',alignContent:'center',boxAlign:'center'}}>
        {(isLogged() ===1) &&
          <Box className={'content'}>
              <Paper style={{textAlign:'center'}}>
              <img src={require("./Logo.png")} style={{alignSelf:'center', maxWidth:'100%',maxHeight:'100%'}} alt="Error en el Logo."/>
              <Typography variant={'h6'}>Introduzca el teléfono de móvil o pulse el botón 'Registrese'</Typography>
              <br/>
              <div style={{float:'left', width:'100%'}}>
              <p style={{padding:'0%', margin:'0%'}}>Teléfono:   <Input type={'text'}/></p>
              </div>
             
             
              <span><Button label={'Registrese'}/> <Button label={'Enviar'}/> </span>
              </Paper>
          </Box>
        }
      
      </div>
      );
  }
}

export default Login;