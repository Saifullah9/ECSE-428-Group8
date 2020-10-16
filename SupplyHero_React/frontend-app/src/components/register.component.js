import React, { Component } from 'react';

export default class Register extends Component{
    constructor(props){
        super(props);

        this.onChangeEmail = this.onChangeEmail.bind(this);
        this.onChangePassword = this.onChangePassword.bind(this);
        this.onSubmit = this.onSubmit.bind(this);

        this.state = {
            email: '',
            password: '',
        }
    }

    onChangeEmail(e){
        this.setState({
            email: e.target.value
        });
    }

    onChangePassword(e){
        this.setState({
            password: e.target.value
        });
    }

    handleSubmit(e){
        e.preventDefault();

        const user = {
            email:this.state.email,
            password:this.state.password,
        }

        console.log('hello world');

        this.setState({
            email:'',
            password:'',
        })

        fetch('http://localhost:8000/register', {
          method: "POST",
          headers: {
            Accept: "application/json","Content-Type": "application/json"
          },
          body: JSON.stringify({
            email: "test@gmail.com",
            password: "mypassword"
          })
        })
        .then(function(response) {
            return response.json();
        })
        .catch(e => {
            console.log(e)
        })
        //window.location = '/' // reroutes to home page after submitting

    }



    render(){
        return(
            <div>
              <h3>Register</h3>
              <form onSubmit={this.onSubmit}>
                <div className="form-group">
                    <label>Email: </label>
                    <input
                        type="text"
                        required
                        value={this.state.email}
                        placeholder="Enter your email"
                        className="form-control"
                        onChange={this.onChangeEmail}
                    />
                    <label>Password: </label>
                    <input
                        type="text"
                        required
                        value={this.state.password}
                        placeholder="Enter your password"
                        className="form-control"
                        onChange={this.onChangePassword}
                    />
                    </div>
                    <div className="form-group">
                <input type="submit" value="Register" onSubmit={this.handleSubmit} className="btn btn-primary" />
                </div>
              </form>
            </div>
        )
    }
}