# main page
'https://opencorporates.com/'

# click to login button
'<a itemprop="url" href="https://opencorporates.com/users/sign_in" class="nav-link"><span itemprop="name">Login</span></a>'

# create an account button
'<a class="btn btn-small btn-info register-link" href="/users/sign_up">Create an account</a>'

# CREATION PAGE

# name input (email w/o @...com)
'<input id="user_name" name="user[name]" type="text">'

# email input (new email)
'<input id="user_email" name="user[email]" type="email" value="">'

# job title input (random string)
'<input id="user_user_info_job_title" name="user[user_info][job_title]" type="text">'

# company/organization (random string)
'<input id="user_user_info_company" name="user[user_info][company]" type="text">'

# password input (same as name)
'<input id="user_password" name="user[password]" type="password">'

# confirm password input
'<input id="user_password_confirmation" name="user[password_confirmation]" type="password">'

# !condition box scroll
'<div class="terms-conditions-box">'

# ?check box after scrolling
'<input class="terms-conditions-checkbox" id="user_terms_and_conditions" name="user[terms_and_conditions]" type="checkbox" value="1">'

# ?check box before scrolling
'<input class="terms-conditions-checkbox" disabled="disabled" id="user_terms_and_conditions" name="user[terms_and_conditions]" type="checkbox" value="1">'

# !!ReCapcha!!

# *Register new account button
'<input class="btn btn-primary" name="commit" type="submit" value="Register new account">'
