/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-uk3m9v4d.eu.auth0.com', // the auth0 domain prefix
    audience: 'coffe', // the audience set for the auth0 app
    clientId: 'lG8UrDPj2IvMUaykRlFRyaVi0vRoUVRW', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
