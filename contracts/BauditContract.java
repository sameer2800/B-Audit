package com.credits.baudit.contracts;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;

public class BauditContract extends SmartContract {
	
	private final String contractOwner;
	private long wallet;
	private final Set<House> houses;
	private MarketPlace marketPlace;
	
	public BauditContract(MarketPlace marketPlace) {		
		//this.contractOwner = msg.sender;
		this.contractOwner = "owner's public key";
		this.houses = new HashSet<House>();
		this.marketPlace = marketPlace;
	}
	
	public void registerHouse(House house) {
		//require(msg.sender == contractOwner);
		houses.add(house);
	}

	public void deRegisterHouse(House house) {
		//require(msg.sender == contractOwner);
		houses.remove(house);
	}
	
	/*
	 this will be called periodically by the contract itself to find all the devices scheduled for 
	 maintainence. contract automatically posts auctions in the market place. then contract fetches 
	 all the bids and selects the best bid and will sanction him the repair. post repair, funds will be
	 transferred.
	 */
	public void scheduleMaintainence() {
		ArrayList<Device> devices = fetchFaultyDevices();
		ArrayList<Auction> auctions = new ArrayList<>();
		
		for(Device device : devices) {
			Auction newAuction = postAnAuction(device);
			auctions.add(newAuction);
		}
		
		for(Auction auction : auctions) {
			AuctionBid auctionBid = selectBestBidder(auction.getId());
			auctionBid.getContractor().transfer( auctionBid.getBidPrice());
			wallet = wallet - auctionBid.getBidPrice();
		}
	}
	
	
	/*iterate over all houses and fetch all the devices which are scheduled for maintainence.
	 * Example : a geyser's one year service. 
	 *  
	*/
	public ArrayList<Device> fetchFaultyDevices() {
		
		ArrayList<Device> faultyDevices = new ArrayList<>();
		for (House house : houses) {
			for(Device device : house.getDevices()) {
				if(GeneralUtils.isFaultyDevice(device)) {
					faultyDevices.add(device);
				}
			}
		}
		return faultyDevices;
	}
	
	
	//this method can be called directly by an IOT device when it finds an faulty device like geyser, light....
	public Auction postAnAuction(Device device) {
		int basePrice = 10;
		Auction createAuction = new Auction("random-id", device, basePrice);
		marketPlace.postAnAuction(createAuction);
		return createAuction;
	}
	
	public AuctionBid selectBestBidder(String id) {
		ArrayList<AuctionBid> bids= marketPlace.fetchBidsforAnAuction(id);
		return GeneralUtils.selectBestBid(bids);
	}
	
}
