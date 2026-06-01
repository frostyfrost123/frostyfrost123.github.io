@RestController
@CrossOrigin(origins = "", allowedHeaders = "")
@RequestMapping("/v1/wallet")
public class WalletController {
  public record DepositPostbackRequest(String userId, BigDecimal amount, String currencyCode, String transactionId) {}

  @PostMapping("/deposit-postback")
  public ResponseEntity<String> handleDepositDone(
          @RequestBody DepositPostbackRequest request,
          @RequestHeader(value = "X-API-KEY") String apiKey) {
      if (apiKey == null || !apiKey.equals("secretValue")) {
          return ResponseEntity.status(HttpStatusCode.UNAUTHORIZED).body("Unauthorized");
      }
      BigDecimal amount = request.amount();
      if (amount == null || amount.signum() != 1) {
          return ResponseEntity.status(HttpStatusCode.BAD_REQUEST).body("Amount must be positive");
      }
      // Calculate new tokens from this deposit (Rounding Up)
      long newTokens = amount.multiply(BigDecimal.valueOf(2.5))
              .setScale(0, RoundingMode.CEILING).longValue();

      increaseUserBalance(request.userId(), newTokens);
      return ResponseEntity.ok("OK");
  }
}
