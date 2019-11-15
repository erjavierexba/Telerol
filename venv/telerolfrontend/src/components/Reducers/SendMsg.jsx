import {SendMSG,DontSendMSG} from './../Actions/SendMsg'
  const initialState = {Accion: DontSendMSG,text: ""}
  
export function SendMSG(state = initialState, action) {
    switch (action.type) {
      case SendMSG:
        return {...state, ...action }
      default:
        return state
    }
  }
  