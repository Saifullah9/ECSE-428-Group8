import React, { Component } from 'react';
import ImageUpload from '../ImageUpload/ImageUpload'

export default class Upload extends Component{
    render(){
        return(
            <div>
            	<div>
            		<ImageUpload />
            	</div>
            	<br></br>
            	<hr/>
            	<br></br>

            	<div>
            		<center>
            		<h3>Image Text</h3>
            		<form>
             			<textarea id="imageTextBox" cols="150" rows="5">pens pencils erasers etc</textarea>
            			<br></br>
            			<input type="submit" value="Confirm and Submit Text"/>
            		</form>
            		</center>
            	</div>
        	</div>
               
        )
    }
}