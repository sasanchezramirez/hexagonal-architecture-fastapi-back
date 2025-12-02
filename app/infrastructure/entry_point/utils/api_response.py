from app.domain.model.util.response_codes import ResponseCodeEnum, ResponseCode
from app.domain.model.util.custom_exceptions import CustomException

class ApiResponse:
    """
    Utility class for creating standardized API responses.
    """
    @staticmethod
    def create_response(response_enum: ResponseCodeEnum, data=None):
        """
        Creates a success response.
        
        Args:
            response_enum: Enum with response code and message.
            data: Optional data to include in the response.
            
        Returns:
            dict: Standardized response dictionary.
        """
        response_code = ResponseCode(response_enum)
        return {
            "apiCode": response_code.code,
            "data": data,
            "message": response_code.message,
            "status": response_code.http_status == 200
        }
    
    @staticmethod
    def create_error_response(exception: CustomException):
        """
        Creates an error response from a custom exception.
        
        Args:
            exception: The custom exception to handle.
            
        Returns:
            dict: Standardized error response dictionary.
        """
        return {
            "apiCode": exception.code,
            "data": None,
            "message": exception.message,
            "status": exception.http_status == 200
        }
