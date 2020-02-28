import{axios} from 'axios';
export const SendLOGIN = 'SendLOGIN';
export const SendLOGINSUCC = 'SendLOGINSUCC';
export const SendLOGINFAIL = 'SendLOGINFAIL';



export const sendLogin = ({ telf }) => {
  return (dispatch) => {
    return axios.post(`apiUrl/add`, {telf})
      .then(response => {
        dispatch({type:SendLOGINSUCC,data:(response.data)})
      })
      .catch(error => {
        throw(error);
      });
  };
};
