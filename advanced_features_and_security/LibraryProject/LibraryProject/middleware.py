
# LibraryProject/middleware.py
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class ContentSecurityPolicyMiddleware(MiddlewareMixin):
    """
    Adds a Content-Security-Policy header to responses.
    Modify the policy variables in settings.py if needed.
    """

    def process_response(self, request, response):
        policy_parts = []
        default_src = " ".join(settings.CSP_DEFAULT_SRC) if hasattr(settings, "CSP_DEFAULT_SRC") else "'self'"
        script_src = " ".join(settings.CSP_SCRIPT_SRC) if hasattr(settings, "CSP_SCRIPT_SRC") else "'self'"
        style_src = " ".join(settings.CSP_STYLE_SRC) if hasattr(settings, "CSP_STYLE_SRC") else "'self'"
        img_src = " ".join(settings.CSP_IMG_SRC) if hasattr(settings, "CSP_IMG_SRC") else "'self'"

        policy_parts.append(f"default-src {default_src}")
        policy_parts.append(f"script-src {script_src}")
        policy_parts.append(f"style-src {style_src}")
        policy_parts.append(f"img-src {img_src}")

        csp_header = "; ".join(policy_parts)
        response["Content-Security-Policy"] = csp_header
        return response
