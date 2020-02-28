import React, { Component } from 'react';
import {Paper, Button,Typography,Input, Grid} from '@material-ui/core';
import {sendLogin} from './../Actions/LoginVer';
import {connect} from 'react-redux';
import Axios from 'axios';


class _Login extends Component {
  constructor(props){
   super(props);
   this.state={ telf:'',}
    this.onChange = this.onChange.bind(this);
    this.send = this.send.bind(this);
  }
  send(){
    Axios.get('http://92.177.190.5:8000/login/'+this.state.telf).then(response => console.log(response));
  }
  onChange(e){
    this.setState({telf:e.target.value});
  }
  render(){
    return (
      <div style={{width:'100%',height:'100%'}}>
            <Grid container direction={'row'} justify={'center'} style={{width:'100%',height:'100%'}}>
              <Grid item xs={6} style={{width:'100%',height:'100%'}}>
                <Grid container direction={'column'} justify={'center'} style={{width:'100%',height:'100%'}}>
                    <Grid item xs={12}  style={{width:'100em',textAlign:'center'}}>
                    <Grid container direction={'row'} justify={'center'} alignItems="center" style={{width:'100%',height:'100%'}}>
                      <Grid item xs={8} >
                        <Paper style={{textAlign:'center'}}>
                          <img src={require("./Logo.png")} style={{alignSelf:'center', maxWidth:'100%',maxHeight:'100%', margin:'14px'}} alt="Error en el Logo."/>
                          <Typography variant={'h6'}>Introduzca el teléfono de móvil o pulse el botón 'Registrese'</Typography>
                          <br/>
                          <div style={{float:'left', width:'100%'}}>
                            <Grid container justify={'center'}><p style={{padding:'0%', margin:'0%'}}>Teléfono:   </p><Input onChange={this.onChange} type={'text'}  style={{marginLeft:'5%'}}/></Grid>
                          </div>
                          <div style={{float:'left', width:'100%'}}>
                            <Button variant="contained" style={{margin:'7.5%'}} onClick={()=>console.log('Obamacare')}>Registrese</Button><Button variant="contained" style={{margin:'7.5%'}} onClick={this.send}>Enviar</Button> 
                          </div>
                          <p style={{marginBottom:'1.5%'}}>Telerol, todos los derechos reservados.</p>
                        </Paper>
                      </Grid>
                    </Grid>
                  </Grid>
                </Grid>
              </Grid>
            </Grid>
          </div>
      );
  }
}
const mapStateToProps = (state) => {
  return { things: state.things }
};
const mapDispatchToProps = () => {
  return {
      sendLogin: sendLogin,
  }
}

export const Login = connect(mapStateToProps,mapDispatchToProps)(_Login);