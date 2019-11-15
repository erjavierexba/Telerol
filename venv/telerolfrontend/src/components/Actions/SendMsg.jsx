
export const SendMSG = 'SendMSG'
export const DontSendMSG = 'DontSendMSG'


export function sendMSG(text) {
  return { type: SendMSG, text:text }
}
export function dontSendMSG() {
    return { type: DontSendMSG, text: "" }
  }