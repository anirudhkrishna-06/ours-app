import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from python_http_client import exceptions
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.sg = sendgrid.SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))
        self.from_email = Email(os.getenv('SENDGRID_FROM_EMAIL', 'noreply@oursemotional.com'))
        self.enabled = bool(os.getenv('SENDGRID_API_KEY'))

    async def send_invitation_email(self, invitation_data: Dict) -> bool:
        """
        Send beautiful emotional invitation email via SendGrid
        """
        if not self.enabled:
            logger.info("Email service disabled - would send invitation to: %s", invitation_data.get('toEmail'))
            return True  # Return True in development

        try:
            to_email = To(invitation_data['toEmail'])
            subject = f"💖 You're Invited to Join {invitation_data['fromUserName']}'s Emotional Space"
            
            # Create beautiful HTML email
            html_content = self._create_invitation_html(invitation_data)
            plain_content = self._create_invitation_text(invitation_data)
            
            content = Content("text/html", html_content)
            mail = Mail(self.from_email, to_email, subject, content)
            
            # Add plain text alternative
            mail.add_content(Content("text/plain", plain_content))
            
            # Send email
            response = self.sg.client.mail.send.post(request_body=mail.get())
            
            if response.status_code in [200, 202]:
                logger.info("✅ Invitation email sent successfully to: %s", invitation_data['toEmail'])
                return True
            else:
                logger.error("❌ Failed to send email. Status: %s, Body: %s", 
                           response.status_code, response.body)
                return False
                
        except exceptions.BadRequestsError as e:
            logger.error("❌ SendGrid API error: %s", e)
            return False
        except Exception as e:
            logger.error("❌ Unexpected email error: %s", e)
            return False

    def _create_invitation_html(self, invitation: Dict) -> str:
        """Create beautiful HTML email content"""
        app_url = os.getenv('APP_URL', 'https://oursemotional.com')
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    margin: 0;
                    padding: 40px 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 20px;
                    overflow: hidden;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                }}
                .header {{
                    background: linear-gradient(135deg, #ff6b8b, #6bc5c5);
                    padding: 50px 40px;
                    text-align: center;
                    color: white;
                }}
                .header h1 {{
                    font-size: 2.5em;
                    margin: 0 0 10px 0;
                    font-weight: 300;
                }}
                .content {{
                    padding: 40px;
                    color: #333;
                    line-height: 1.6;
                }}
                .message-box {{
                    background: #f8f9fa;
                    border-left: 4px solid #ff6b8b;
                    padding: 20px;
                    margin: 25px 0;
                    border-radius: 8px;
                    font-style: italic;
                }}
                .code-display {{
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white;
                    padding: 25px;
                    border-radius: 15px;
                    text-align: center;
                    margin: 30px 0;
                    font-size: 1.8em;
                    font-weight: bold;
                    letter-spacing: 2px;
                }}
                .button {{
                    display: inline-block;
                    background: linear-gradient(135deg, #ff6b8b, #6bc5c5);
                    color: white;
                    padding: 16px 40px;
                    text-decoration: none;
                    border-radius: 50px;
                    font-size: 1.1em;
                    font-weight: 600;
                    margin: 20px 0;
                    transition: transform 0.3s ease;
                }}
                .button:hover {{
                    transform: translateY(-2px);
                }}
                .footer {{
                    text-align: center;
                    padding: 30px;
                    background: #f8f9fa;
                    color: #666;
                    font-size: 0.9em;
                }}
                .heart {{
                    color: #ff6b8b;
                    font-size: 1.2em;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>💖 You're Invited!</h1>
                    <p style="font-size: 1.2em; opacity: 0.9;">
                        Join {invitation['fromUserName']} in Our's Emotional Space
                    </p>
                </div>
                
                <div class="content">
                    <h2 style="color: #333; margin-bottom: 20px;">A Sacred Space Awaits You</h2>
                    
                    <p>Hello beautiful soul,</p>
                    
                    <p>{invitation['fromUserName']} has created a special emotional sanctuary for your relationship and would be honored to have you join them.</p>
                    
                    <div class="message-box">
                        "{invitation['personalMessage']}"
                    </div>
                    
                    <p>This is your invitation to create a private space where your relationship can grow, heal, and flourish together.</p>
                    
                    <h3 style="color: #333; text-align: center; margin: 30px 0 20px 0;">
                        Your Connection Code
                    </h3>
                    
                    <div class="code-display">
                        {invitation['connectionCode']}
                    </div>
                    
                    <div style="text-align: center;">
                        <a href="{app_url}/accept-invitation?code={invitation['connectionCode']}" class="button">
                            Accept This Beautiful Invitation
                        </a>
                    </div>
                    
                    <p style="text-align: center; color: #666; font-size: 0.9em;">
                        This invitation expires on {invitation['expiresAt'].strftime('%B %d, %Y')}<br>
                        Code: {invitation['connectionCode']}
                    </p>
                </div>
                
                <div class="footer">
                    <p>Sent with <span class="heart">💖</span> from <strong>Our's</strong> - Your Relationship Emotional Space</p>
                    <p>Create moments. Grow together. Love deeply.</p>
                </div>
            </div>
        </body>
        </html>
        """

    def _create_invitation_text(self, invitation: Dict) -> str:
        """Create plain text version for email clients"""
        app_url = os.getenv('APP_URL', 'https://oursemotional.com')
        
        return f"""
        You're Invited to Our's Emotional Space! 💖

        Dear Friend,

        {invitation['fromUserName']} has invited you to join their emotional sanctuary in Our's.

        Personal Message:
        "{invitation['personalMessage']}"

        Our's is a private space where relationships grow through:
        • Sharing beautiful memories
        • Emotional reflection and understanding  
        • Growing together consciously
        • Healing and connection

        YOUR CONNECTION CODE: {invitation['connectionCode']}

        To accept this invitation:
        1. Visit: {app_url}
        2. Click "Accept Invitation" 
        3. Enter this code: {invitation['connectionCode']}

        Or click this direct link:
        {app_url}/accept-invitation?code={invitation['connectionCode']}

        This invitation expires on: {invitation['expiresAt'].strftime('%B %d, %Y')}

        Sent with love from Our's - Your Relationship Emotional Space
        Create moments. Grow together. Love deeply.
        """

# Singleton instance
email_service = EmailService()