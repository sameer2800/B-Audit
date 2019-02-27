package com.credits.baudit.contracts;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class MarketPlace extends SmartContract {
	
	private final Set<Contractor> contractors;
	private String MPDetails;
	private Map<String,Auction>auctions;
	
	public MarketPlace() {
		contractors = new HashSet<Contractor>();
		auctions = new HashMap<String,Auction>();
	}
	
	public void postAnAuction(Auction auction) {
		auctions.put( auction.getId(), auction);
	}
	
	public ArrayList<AuctionBid> fetchBidsforAnAuction(String auctionId) {
		return auctions.get(auctionId).getAuctionBids();
	}
}
